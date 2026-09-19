---
language:
- en
- hi
- as
license: mit
library_name: peft
tags:
- weather
- meteorology
- agromet
- indic
- climate-science
- imd
- open-meteo
- gfs
- tool-calling
datasets:
- sih26068/weathergpt-indic-bench-50k
metrics:
- accuracy
- tool_selection_accuracy
- latency
model_name: WeatherGPT-Indic-8B-Instruct
base_model: meta-llama/Meta-Llama-3-8B-Instruct
pipeline_tag: text-generation
---

# 🌦️ Model Card: WeatherGPT-Indic-8B-Instruct

> ⚠️ **Status: draft / not trained.** This card describes a *target* model. No adapter has been trained or published from this repository (`scripts/train_indic_lora.py` generates a corpus and LoRA configuration only), and the adapter repository referenced below does not exist. Metrics are omitted rather than estimated.

**WeatherGPT-Indic-8B-Instruct** is an Indic multilingual parameter-efficient instruction-tuned model designed for conversational meteorological intelligence, official India Meteorological Department (IMD) bulletin reasoning, Numerical Weather Prediction (NWP/GFS) interpretation, and Gramin Krishi Mausam Sewa (GKMS) agricultural advisory generation.

The model natively supports **English**, **Hindi**, and **Assamese** (`as`), providing localized agricultural insights (paddy, tea, mustard, jute, wheat) and severe weather safety guidance across Northeast and Pan-India agro-climatic zones.

---

## 🔬 Model Summary

- **Developed by:** SIH26068 WeatherGPT Development Team
- **Base Model:** `meta-llama/Meta-Llama-3-8B-Instruct`
- **Methodology:** QLoRA / PEFT with Rank $r=16$, $\alpha=32$, targeting all linear projection layers (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`).
- **Primary Languages:** English (`en`), Hindi (`hi`), Assamese (`as`).
- **Domain Specialization:** Numerical Weather Prediction (NWP), WMO Code Mapping, Severe Convection & CAPE Soundings, Agro-meteorological Advisories, Indigenous Climate Phenomena (Bordoisila, Kalbaishakhi, Western Disturbances, Southwest Monsoon, ENSO/IOD).

---

## 📊 Benchmark Evaluation Metrics

**Not measured.** No adapter has been trained, so no model metrics exist. Figures previously listed in this card were not reproducible from this repository and have been removed.

For the *agent's* behaviour on the 50-item rubric (tool routing, language consistency, keyword recall, response length — not model quality), see [`evals/RESULTS.md`](../../evals/RESULTS.md).

---

## 🛠️ Tool Calling & Schema Support

WeatherGPT is trained to output JSON-schema structured tool calls against the following backend functions:

1. `get_current_weather(location)`: Fetches real-time temperature, humidity, wind, and WMO codes.
2. `get_forecast(location, days)`: Returns 7-day daily and hourly forecast curves.
3. `get_air_quality(location)`: Retrieves PM2.5, PM10, AQI, and health recommendations.
4. `get_imd_alerts(location)`: Parses official IMD color-coded warnings (Green/Yellow/Orange/Red).
5. `get_gfs_prediction(location)`: Calculates atmospheric convective instability (CAPE) and synoptic soundings.
6. `get_agromet_advisory(crop, location)`: GKMS farming directives for irrigation, drainage, and spray windows.
7. `search_climate_knowledge(query)`: High-accuracy meteorological phenomena lookup.

---

## 🚀 Quickstart & Inference

*(Illustrative: the adapter below has not been published — see the status note at the top of this card.)*

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
adapter_id = "sih26068/weathergpt-indic-8b-adapter"

tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, adapter_id)

prompt = """<|im_start|>system
You are WeatherGPT, an official Indic meteorological intelligence agent.<|im_end|>
<|im_start|>user
কাইলৈ ডিব্ৰুগড়ত চাহ খেতিৰ বাবে বৰষুণৰ সম্ভাৱনা আৰু পৰামৰ্শ কি?<|im_end|>
<|im_start|>assistant
"""

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.3)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 📜 Ethical Considerations & Limitations
- Weather forecasts inherently contain atmospheric uncertainty. High-risk maritime or aviation operations must cross-verify with official IMD Doppler radar and radar nowcast portals.
