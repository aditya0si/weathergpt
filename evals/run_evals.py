"""WeatherGPT 50-Item Multilingual Benchmark Evaluation Harness.

The harness scores the live agent against a fixed rubric (tool selection,
language consistency, keyword recall, response length) and can be used as a CI
gate via --fail-under.

It also reports the *data provenance* of the run: whether each case was answered
from live upstream APIs (Open-Meteo) or from the offline synthetic fallback, so
a reported score can never be mistaken for a fully live-data measurement.
"""

import argparse
import asyncio
import json
import math
import os
import sys
import time
from typing import Any, Dict, List

from tabulate import tabulate

from weathergpt.agent.engine import weather_agent
from weathergpt.core.models import ChatRequest

DEFAULT_FAIL_UNDER = 85.0


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


def _iter_sources(tool_calls: List[Any]) -> List[str]:
    """Yields the `source` strings reported by the tools that ran for one case."""
    sources: List[str] = []
    for call in tool_calls:
        result = call.result
        if isinstance(result, dict) and isinstance(result.get("source"), str):
            sources.append(result["source"])
        elif isinstance(result, list):
            for item in result:
                if isinstance(item, dict) and isinstance(item.get("source"), str):
                    sources.append(item["source"])
    return sources


# Explicit provenance markers. Prose is not parsed loosely: an honest string such
# as "not a live IMD feed" must not be read as a live-data marker.
SYNTHETIC_MARKERS = ("synthetic", "fabricated", "not a measurement")
LIVE_MARKERS = ("live api", "(live)")


def classify_provenance(tool_calls: List[Any]) -> str:
    """Classifies where a case's answer data came from.

    Returns one of:
      - "synthetic-fallback": at least one tool served locally generated
        (synthetic) data instead of an upstream reading.
      - "live-upstream": at least one tool served live upstream data and none
        served synthetic data.
      - "offline-static": no tool used an upstream data source (static knowledge
        base, static alert reference set, or analytic estimate only).
    """
    sources = [s.lower() for s in _iter_sources(tool_calls)]
    if any(marker in s for s in sources for marker in SYNTHETIC_MARKERS):
        return "synthetic-fallback"
    if any(marker in s for s in sources for marker in LIVE_MARKERS):
        return "live-upstream"
    return "offline-static"


async def run_benchmark(
    dataset_path: str,
    results_output_path: str,
    fail_under: float = DEFAULT_FAIL_UNDER,
) -> Dict[str, Any]:
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
    provenance_counts = {"live-upstream": 0, "synthetic-fallback": 0, "offline-static": 0}

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

        provenance = classify_provenance(resp.tool_calls)
        provenance_counts[provenance] += 1

        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(score)
        lang_scores[lang].append(score)

        status_emoji = "✅" if score >= 80.0 else "⚠️"
        print(f"[{i:02d}/50] {status_emoji} {cid} ({lang.upper()}) | Cat: {cat:<16} | Tools: {called_tools} | "
              f"Data: {provenance} | Score: {score:.1f}% | Latency: {elapsed_ms:.1f}ms")

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
            "provenance": provenance,
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
    generated_at = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())

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
        ["Cases answered from live upstream data", provenance_counts["live-upstream"]],
        ["Cases answered from the synthetic fallback", provenance_counts["synthetic-fallback"]],
        ["Cases with no upstream call (static KB / analytic estimate)", provenance_counts["offline-static"]],
    ]

    print("\n" + "=" * 80)
    print("📊 BENCHMARK EVALUATION SUMMARY")
    print("=" * 80)
    print(tabulate(summary_table, headers=["Metric", "Result"], tablefmt="fancy_grid"))

    print("\n🌐 ACCURACY BY LANGUAGE")
    print(tabulate(lang_table_rows, headers=["Language", "Count", "Accuracy"], tablefmt="grid"))

    print("\n📁 ACCURACY BY DOMAIN CATEGORY")
    print(tabulate(cat_table_rows, headers=["Category", "Count", "Accuracy"], tablefmt="grid"))

    if provenance_counts["synthetic-fallback"]:
        print(
            f"\n⚠️  {provenance_counts['synthetic-fallback']}/{len(results)} cases were answered from the "
            "synthetic fallback generator because an upstream API was unavailable: those cases measure "
            "agent routing and response formatting, not upstream data accuracy."
        )

    # Write RESULTS.md
    markdown_content = f"""# WeatherGPT Indic Multilingual Benchmark Results

> Generated by `python evals/run_evals.py` on {generated_at} (UTC).
> Latency figures are specific to the machine and network path of that run;
> the correctness / tool-selection figures are reproducible for the same commit.

## Data provenance for this run
| Provenance | Cases |
| :--- | :---: |
| Live upstream data (Open-Meteo) | {provenance_counts['live-upstream']} |
| Synthetic fallback (upstream unavailable) | {provenance_counts['synthetic-fallback']} |
| No upstream call (static KB / analytic estimate) | {provenance_counts['offline-static']} |

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
    markdown_content += "| ID | Lang | Category | Prompt | Tools Executed | Data | Score | Latency |\n"
    markdown_content += "| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: |\n"
    for r in results[:15]:
        tools_str = ", ".join(r["called_tools"])
        markdown_content += (f"| `{r['id']}` | {r['language'].upper()} | {r['category']} | {r['prompt'][:45]}... | "
                             f"`{tools_str}` | {r['provenance']} | {r['score']}% | {r['latency_ms']}ms |\n")

    with open(results_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\n✅ Results report generated at: {results_output_path}")

    if total_avg_score < fail_under:
        print(
            f"\n❌ GATE FAILED: overall correctness {total_avg_score}% is below the required floor of {fail_under}%.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\n✅ GATE PASSED: overall correctness {total_avg_score}% >= required floor of {fail_under}%.")

    return {
        "total_cases": len(results),
        "avg_score": total_avg_score,
        "tool_accuracy": avg_tool_acc,
        "p50_latency_ms": p50_lat,
        "p95_latency_ms": p95_lat,
        "provenance_counts": provenance_counts,
    }


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="WeatherGPT 50-item multilingual benchmark harness")
    parser.add_argument(
        "--dataset",
        default=os.path.join(base_dir, "data", "weathergpt_eval_50.json"),
        help="Path to the evaluation dataset JSON",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(base_dir, "RESULTS.md"),
        help="Where to write the markdown results report",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=DEFAULT_FAIL_UNDER,
        help=f"Exit non-zero if overall correctness is below this value (default: {DEFAULT_FAIL_UNDER})",
    )
    args = parser.parse_args()

    asyncio.run(run_benchmark(args.dataset, args.output, args.fail_under))


if __name__ == "__main__":
    main()
