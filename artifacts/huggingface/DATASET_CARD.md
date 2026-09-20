---
language:
- en
- hi
- as
license: mit
task_categories:
- question-answering
- text2text-generation
tags:
- weather
- indic
- assam
- agromet
- climate-science
- imd
- tool-calling
size_categories:
- 10K<n<100K
---

# 📚 Dataset Card: IndicWeather-Bench-50k & Eval-50

> ⚠️ **Status: partially published.** Only the 50-item evaluation set (`evals/data/weathergpt_eval_50.json`) is included in this repository. The 50,000-sample training corpus is **not** included or published; the counts below describe the intended dataset, not shipped data.

## Dataset Description
**IndicWeather-Bench-50k** is a trilingual (English, Hindi, Assamese) meteorological reasoning and tool-calling dataset curated for SIH26068 (WeatherGPT). It is paired with the standardized **WeatherGPT-50** golden evaluation set designed to benchmark conversational agents on multi-turn weather queries, agricultural advisories, severe disaster warnings, and climate science Q&A.

---

## 🌐 Language Coverage & Distributions

| Language | ISO 639-1 | Region | Training Samples | Eval Benchmark |
| :--- | :---: | :--- | :---: | :---: |
| **English** | `en` | Pan-India / International | 25,000 | 20 |
| **Hindi** | `hi` | North & Central India | 15,000 | 15 |
| **Assamese** | `as` | Assam & Northeast India | 10,000 | 15 |
| **Total** | — | — | **50,000** | **50** |

---

## 📁 Domain Categorization

1. **Current Meteorological Observation**: Temperature, Feels Like, Humidity, Wind Vector, Cloud Cover, Barometric Pressure.
2. **7-Day Numerical Forecast**: Precipitation sum, Rain Probability curves, diurnal temperature cycles.
3. **IMD Severe Weather Bulletins**: Color-coded alerts (Green, Yellow, Orange, Red), Heavy Rainfall, Cyclones, Heatwaves, Cold Waves, Fog.
4. **Agro-Meteorological (GKMS) Advisories**: Crop stage diagnostics for Paddy (Sali/Ahu), Tea, Mustard, Wheat, Jute, Horticulture; irrigation timings, spray safety windows.
5. **Air Quality Index (AQI)**: PM2.5, PM10, NO2, SO2, CO pollutant concentrations and CPCB health advisories.
6. **Climate Science & Atmospheric Physics**: Southwest Monsoon onset/withdrawal, Bordoisila & Kalbaishakhi pre-monsoon squalls, Western Disturbances, El Niño / IOD coupled oceanic teleconnections, Urban Heat Islands.

---

## 📋 JSON Schema Example

```json
{
  "id": "eval_as_06",
  "language": "as",
  "category": "climate_qa",
  "prompt": "অসমৰ বৰদৈচিলা ধুমুহাৰ বৈজ্ঞানিক কাৰণ আৰু লোকবিশ্বাস কি?",
  "expected_tools": ["search_climate_knowledge"],
  "expected_keywords": ["বৰদৈচিলা", "ধুমুহা", "বংগোপসাগৰ", "মাকৰ ঘৰলৈ"],
  "min_length": 70,
  "description": "Assamese Bordoisila cultural and scientific explanation"
}
```

---

## 🛠️ Usage in Python with `datasets`

```python
from datasets import load_dataset

dataset = load_dataset("sih26068/weathergpt-indic-bench-50k")
print(dataset["train"][0])
```
