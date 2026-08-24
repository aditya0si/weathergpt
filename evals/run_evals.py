"""WeatherGPT 50-Item Multilingual Benchmark Evaluation Harness."""

import asyncio
import json
import math
import os
import time
from typing import Any, Dict, List

from tabulate import tabulate

from weathergpt.agent.engine import weather_agent
from weathergpt.core.models import ChatRequest


def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculates percentile for a list of floats."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return round(d0 + d1, 2)


async def run_benchmark(dataset_path: str, results_output_path: str) -> Dict[str, Any]:
    """Runs the 50-case benchmark evaluation suite."""
    print("=" * 80)
    print("🌦️ WeatherGPT Indic Multilingual Benchmark Evaluation Suite (50 Test Cases)")
    print("=" * 80)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Evaluation dataset not found at {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases: List[Dict[str, Any]] = json.load(f)

    print(f"Loaded {len(cases)} evaluation test cases from {os.path.basename(dataset_path)}.")
    print("Evaluating English, Hindi, and Assamese multi-turn & tool-calling queries...\n")

    results = []
    latencies = []
    category_scores = {}
    lang_scores = {"en": [], "hi": [], "as": []}
    tool_accuracies = []

    for i, case in enumerate(cases, 1):
        cid = case["id"]
        cat = case["category"]
        lang = case["language"]
        prompt = case["prompt"]
        expected_tools = case.get("expected_tools", [])
        expected_kws = [k.lower() for k in case.get("expected_keywords", [])]
        min_len = case.get("min_length", 30)

        t_start = time.perf_counter()
        req = ChatRequest(message=prompt, language=lang)
        resp = await weather_agent.chat(req)
        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)
        latencies.append(elapsed_ms)

        # 1. Tool Selection Check
        called_tools = [c.tool_name for c in resp.tool_calls]
        tool_hit = any(t in called_tools for t in expected_tools)
        tool_accuracies.append(1.0 if tool_hit else 0.0)

        # 2. Language Consistency Check
        lang_match = resp.detected_language == lang

        # 3. Keyword / Concept Recall
        reply_lower = resp.reply.lower()
        matched_kws = [k for k in expected_kws if k in reply_lower]
        kw_coverage = len(matched_kws) / len(expected_kws) if expected_kws else 1.0

        # 4. Length check
        len_valid = len(resp.reply) >= min_len

        # 5. Composite Correctness Score (0-100)
        score = (0.40 * (1.0 if tool_hit else 0.0) +
                 0.25 * (1.0 if lang_match else 0.0) +
                 0.25 * kw_coverage +
                 0.10 * (1.0 if len_valid else 0.0)) * 100.0

        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(score)
        lang_scores[lang].append(score)

        status_emoji = "✅" if score >= 80.0 else "⚠️"
        print(f"[{i:02d}/50] {status_emoji} {cid} ({lang.upper()}) | Cat: {cat:<16} | Tools: {called_tools} | Score: {score:.1f}% | Latency: {elapsed_ms:.1f}ms")

        results.append({
            "id": cid,
            "category": cat,
            "language": lang,
            "prompt": prompt,
            "called_tools": called_tools,
            "score": round(score, 1),
            "tool_hit": tool_hit,
            "lang_match": lang_match,
            "kw_coverage": round(kw_coverage * 100, 1),
            "latency_ms": elapsed_ms,
        })

    # Summary Statistics
    total_avg_score = round(sum(r["score"] for r in results) / len(results), 2)
    avg_tool_acc = round((sum(tool_accuracies) / len(tool_accuracies)) * 100, 2)
    p50_lat = calculate_percentile(latencies, 50)
    p90_lat = calculate_percentile(latencies, 90)
    p95_lat = calculate_percentile(latencies, 95)
    p99_lat = calculate_percentile(latencies, 99)
    avg_lat = round(sum(latencies) / len(latencies), 2)

    cat_table_rows = []
    for cat, scores in category_scores.items():
        cat_table_rows.append([cat, len(scores), f"{sum(scores)/len(scores):.2f}%"])

    lang_table_rows = []
    for lang, scores in lang_scores.items():
        lang_table_rows.append([lang.upper(), len(scores), f"{sum(scores)/len(scores):.2f}%"])

    summary_table = [
        ["Total Test Cases Evaluated", len(results)],
        ["Overall Correctness Score", f"{total_avg_score}%"],
        ["Tool Selection Accuracy", f"{avg_tool_acc}%"],
        ["Average Latency (Mean)", f"{avg_lat} ms"],
        ["p50 Latency (Median)", f"{p50_lat} ms"],
        ["p90 Latency", f"{p90_lat} ms"],
        ["p95 Latency", f"{p95_lat} ms"],
        ["p99 Latency", f"{p99_lat} ms"],
    ]

    print("\n" + "=" * 80)
    print("📊 BENCHMARK EVALUATION SUMMARY")
    print("=" * 80)
    print(tabulate(summary_table, headers=["Metric", "Result"], tablefmt="fancy_grid"))

    print("\n🌐 ACCURACY BY LANGUAGE")
    print(tabulate(lang_table_rows, headers=["Language", "Count", "Accuracy"], tablefmt="grid"))

    print("\n📁 ACCURACY BY DOMAIN CATEGORY")
    print(tabulate(cat_table_rows, headers=["Category", "Count", "Accuracy"], tablefmt="grid"))

    # Write RESULTS.md
    markdown_content = f"""# WeatherGPT Indic Multilingual Benchmark Results

## Executive Summary
Evaluation performed on **{len(results)}** curated multilingual test cases spanning English (`en`), Hindi (`hi`), and Assamese (`as`).

### Key Performance Metrics
| Metric | Value |
| :--- | :--- |
| **Total Test Cases** | {len(results)} |
| **Overall Correctness Score** | **{total_avg_score}%** |
| **Tool Selection Accuracy** | **{avg_tool_acc}%** |
| **Average Latency (Mean)** | {avg_lat} ms |
| **p50 Latency (Median)** | {p50_lat} ms |
| **p90 Latency** | {p90_lat} ms |
| **p95 Latency** | {p95_lat} ms |
| **p99 Latency** | {p99_lat} ms |

### Accuracy by Language
| Language | Test Cases | Correctness |
| :--- | :---: | :---: |
| English (`en`) | {len(lang_scores['en'])} | {sum(lang_scores['en'])/len(lang_scores['en']):.2f}% |
| Hindi (`hi`) | {len(lang_scores['hi'])} | {sum(lang_scores['hi'])/len(lang_scores['hi']):.2f}% |
| Assamese (`as`) | {len(lang_scores['as'])} | {sum(lang_scores['as'])/len(lang_scores['as']):.2f}% |

### Accuracy by Meteorological Domain
| Domain Category | Samples | Correctness |
| :--- | :---: | :---: |
"""
    for cat, scores in category_scores.items():
        markdown_content += f"| {cat.replace('_', ' ').title()} | {len(scores)} | {sum(scores)/len(scores):.2f}% |\n"

    markdown_content += "\n## Detailed Sample Breakdown\n"
    markdown_content += "| ID | Lang | Category | Prompt | Tools Executed | Score | Latency |\n"
    markdown_content += "| :--- | :---: | :--- | :--- | :--- | :---: | :---: |\n"
    for r in results[:15]:
        tools_str = ", ".join(r["called_tools"])
        markdown_content += f"| `{r['id']}` | {r['language'].upper()} | {r['category']} | {r['prompt'][:45]}... | `{tools_str}` | {r['score']}% | {r['latency_ms']}ms |\n"

    with open(results_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\n✅ Results report generated at: {results_output_path}")

    return {
        "total_cases": len(results),
        "avg_score": total_avg_score,
        "tool_accuracy": avg_tool_acc,
        "p50_latency_ms": p50_lat,
        "p95_latency_ms": p95_lat,
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_file = os.path.join(base_dir, "data", "weathergpt_eval_50.json")
    results_file = os.path.join(base_dir, "RESULTS.md")
    asyncio.run(run_benchmark(dataset_file, results_file))
