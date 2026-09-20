"""Indic Weather & AgroMet corpus + LoRA adapter-configuration generator.

Status: **no model training is implemented in this script.** It generates a
synthetic Indic instruction corpus and writes a PEFT/LoRA adapter configuration
so the intended fine-tuning setup is reproducible and reviewable. It does not
load a base model, does not train, and therefore produces no loss, perplexity or
parameter-count metrics.

Real QLoRA training would require the optional `ml` extra (torch, transformers,
peft, datasets, accelerate — see pyproject.toml) plus a GPU; passing
`--synthetic-dry-run` is currently the only supported mode and any request to
train exits with a clear error instead of reporting fabricated metrics.
"""

import argparse
import json
import os
import time
from typing import Any, Dict, List

NOT_IMPLEMENTED_MESSAGE = (
    "Real QLoRA fine-tuning is NOT implemented in this script: it contains no "
    "training loop and would not produce trustworthy metrics. Only "
    "`--synthetic-dry-run` (corpus + adapter configuration generation) is "
    "supported. See README 'Machine Learning & Fine-Tuning Pipeline'."
)


def generate_synthetic_indic_tuning_samples(count: int = 100) -> List[Dict[str, Any]]:
    """Generates synthetic training dataset pairs formatted for ChatML / Alpaca."""
    crops = ["Paddy", "Tea", "Mustard", "Wheat", "Jute"]
    cities = ["Guwahati", "Dibrugarh", "New Delhi", "Lucknow", "Kolkata", "Jorhat", "Shillong"]
    langs = ["en", "hi", "as"]

    samples = []
    for i in range(count):
        crop = crops[i % len(crops)]
        city = cities[i % len(cities)]
        lang = langs[i % len(langs)]

        if lang == "as":
            instruction = f"{city}ত {crop} খেতিৰ বাবে বতৰৰ পৰামৰ্শ দিয়ক।"
            response = f"📍 {city}ৰ বতৰৰ ওপৰত ভিত্তি কৰি {crop} শস্যৰ পৰামৰ্শ: বৰষুণৰ সম্ভাৱনা থাকিলে পানী নিষ্কাশনৰ ব্যৱস্থা কৰক আৰু পৰিষ্কাৰ দিনতহে সাৰ ছটিয়াব।"
        elif lang == "hi":
            instruction = f"{city} में {crop} की फसल के लिए मौसम आधारित कृषि सलाह दें।"
            response = f"📍 {city} के मौसम को देखते हुए {crop} की फसल के लिए सलाह: खेत में जल निकासी सुनिश्चित करें और केवल साफ मौसम में ही कीटनाशक का छिड़काव करें।"
        else:
            instruction = f"Provide agricultural weather advisory for {crop} in {city}."
            response = f"📍 Agro-Meteorological advisory for {crop} in {city}: Maintain proper drainage bunds and delay chemical spraying if precipitation is forecasted."

        samples.append({
            "id": f"sample_{i+1:04d}",
            "language": lang,
            "instruction": instruction,
            "context": f"Current weather in {city}: 28.5°C, humidity 78%, precipitation 4.0mm.",
            "response": response,
        })

    return samples


def run_training_pipeline(args: argparse.Namespace) -> None:
    """Generates the corpus + adapter configuration. Never reports training metrics."""
    if not args.synthetic_dry_run:
        print(NOT_IMPLEMENTED_MESSAGE)
        raise SystemExit(2)

    print("=" * 80)
    print("🚀 WeatherGPT Indic LoRA Dry-Run (corpus + adapter configuration only)")
    print("=" * 80)
    print(f"Base Model:         {args.model_name}")
    print(f"Output Directory:   {args.output_dir}")
    print(f"Planned Epochs:     {args.epochs} (not executed)")
    print(f"Planned Batch Size: {args.batch_size} (not executed)")
    print(f"Planned LR:         {args.learning_rate} (not executed)")
    print(f"LoRA Rank (r):      {args.lora_r}")
    print(f"LoRA Alpha:         {args.lora_alpha}")
    print(f"Target Modules:     {args.target_modules}")
    print("Mode:               DRY RUN — no training is performed")
    print("=" * 80)

    os.makedirs(args.output_dir, exist_ok=True)
    dataset_file = os.path.join(args.output_dir, "indic_training_corpus.json")

    print("\n[Step 1/2] Preparing synthetic Indic meteorological corpus...")
    corpus = generate_synthetic_indic_tuning_samples(count=150)
    with open(dataset_file, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"✅ Generated {len(corpus)} synthetic Indic instruction pairs saved to {dataset_file}")
    print("   (synthetic templates — not a curated or externally sourced dataset)")

    print("\n[Step 2/2] Writing PEFT LoRA configuration...")
    lora_config = {
        "peft_type": "LORA",
        "task_type": "CAUSAL_LM",
        "r": args.lora_r,
        "lora_alpha": args.lora_alpha,
        "lora_dropout": 0.05,
        "target_modules": args.target_modules.split(","),
        "bias": "none",
        "base_model_name_or_path": args.model_name,
    }
    config_save_path = os.path.join(args.output_dir, "adapter_config.json")
    with open(config_save_path, "w", encoding="utf-8") as f:
        json.dump(lora_config, f, indent=2)
    print(f"✅ Saved LoRA adapter configuration to {config_save_path}")

    # Metadata records what actually happened: nothing was trained, so no metric
    # is written. Any downstream consumer must treat this adapter as untrained.
    meta = {
        "model_id": "weathergpt-indic-8b-instruct",
        "base_model": args.model_name,
        "languages": ["en", "hi", "as"],
        "dataset_size_samples": len(corpus),
        "training_performed": False,
        "metrics": None,
        "note": (
            "Dry-run artifact: corpus and LoRA configuration only. No base model was loaded, "
            "no training ran and no loss/perplexity was measured."
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(os.path.join(args.output_dir, "model_meta.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(meta, indent=2) + "\n")

    print("\n" + "=" * 80)
    print("✅ DRY RUN COMPLETE — no training was performed and no metrics were produced.")
    print(f"Artifacts written to: {os.path.abspath(args.output_dir)}")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Indic corpus + LoRA config for WeatherGPT (dry run only)")
    parser.add_argument("--model-name", type=str, default="meta-llama/Meta-Llama-3-8B-Instruct")
    parser.add_argument("--output-dir", type=str, default="artifacts/indic_lora_adapter")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--target-modules", type=str, default="q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj")
    parser.add_argument(
        "--synthetic-dry-run",
        action="store_true",
        default=False,
        help="Generate the synthetic corpus and adapter configuration only (the only supported mode)",
    )

    args = parser.parse_args()
    run_training_pipeline(args)
