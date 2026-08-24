"""Unit tests for the evaluation dataset and benchmark runner."""

import json
import os

from evals.run_evals import calculate_percentile


def test_eval_dataset_integrity():
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "evals", "data", "weathergpt_eval_50.json")
    assert os.path.exists(dataset_path), "Evaluation dataset file missing"

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    assert len(cases) == 50, f"Expected 50 test cases, found {len(cases)}"

    # Check language balance
    langs = [c["language"] for c in cases]
    assert langs.count("en") == 20
    assert langs.count("hi") == 15
    assert langs.count("as") == 15

    # Check required fields
    for case in cases:
        assert "id" in case
        assert "category" in case
        assert "language" in case
        assert "prompt" in case
        assert "expected_tools" in case
        assert len(case["expected_tools"]) > 0


def test_percentile_calculation():
    data = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    p50 = calculate_percentile(data, 50)
    assert 50.0 <= p50 <= 60.0

    p90 = calculate_percentile(data, 90)
    assert p90 >= 90.0
