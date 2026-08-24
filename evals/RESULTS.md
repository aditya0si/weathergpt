# WeatherGPT Indic Multilingual Benchmark Results

## Executive Summary
Evaluation performed on **50** curated multilingual test cases spanning English (`en`), Hindi (`hi`), and Assamese (`as`).

### Key Performance Metrics
| Metric | Value |
| :--- | :--- |
| **Total Test Cases** | 50 |
| **Overall Correctness Score** | **94.59%** |
| **Tool Selection Accuracy** | **100.0%** |
| **Average Latency (Mean)** | 1015.69 ms |
| **p50 Latency (Median)** | 771.31 ms |
| **p90 Latency** | 2432.38 ms |
| **p95 Latency** | 2519.52 ms |
| **p99 Latency** | 3434.25 ms |

### Accuracy by Language
| Language | Test Cases | Correctness |
| :--- | :---: | :---: |
| English (`en`) | 20 | 98.33% |
| Hindi (`hi`) | 15 | 91.53% |
| Assamese (`as`) | 15 | 92.64% |

### Accuracy by Meteorological Domain
| Domain Category | Samples | Correctness |
| :--- | :---: | :---: |
| Current Weather | 9 | 94.44% |
| Forecast | 7 | 89.88% |
| Imd Alerts | 5 | 93.33% |
| Air Quality | 4 | 95.83% |
| Agromet | 11 | 97.35% |
| Climate Qa | 12 | 94.79% |
| Gfs Physics | 2 | 95.83% |

## Detailed Sample Breakdown
| ID | Lang | Category | Prompt | Tools Executed | Score | Latency |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| `eval_en_01` | EN | current_weather | What is the current temperature and humidity ... | `get_current_weather, get_imd_alerts` | 100.0% | 863.78ms |
| `eval_en_02` | EN | forecast | Give me the 7-day weather forecast for New De... | `get_forecast, get_imd_alerts` | 100.0% | 731.7ms |
| `eval_en_03` | EN | imd_alerts | Are there any severe weather alerts or rain w... | `get_imd_alerts, get_current_weather` | 91.7% | 699.96ms |
| `eval_en_04` | EN | air_quality | What is the AQI and PM2.5 air pollution level... | `get_air_quality, get_current_weather` | 100.0% | 1733.06ms |
| `eval_en_05` | EN | agromet | I am growing tea in Jorhat. What is the agric... | `get_agromet_advisory, get_current_weather` | 100.0% | 1367.76ms |
| `eval_en_06` | EN | agromet | How should I manage irrigation for paddy crop... | `get_agromet_advisory, get_current_weather` | 100.0% | 1371.81ms |
| `eval_en_07` | EN | climate_qa | Explain what Bordoisila means in Assam meteor... | `search_climate_knowledge` | 100.0% | 1.32ms |
| `eval_en_08` | EN | climate_qa | How do Western Disturbances bring winter rain... | `search_climate_knowledge` | 100.0% | 0.13ms |
| `eval_en_09` | EN | climate_qa | What is the relationship between El Nino and ... | `search_climate_knowledge` | 87.5% | 0.1ms |
| `eval_en_10` | EN | gfs_physics | Show me the GFS numerical sounding and CAPE a... | `get_gfs_prediction, get_current_weather` | 100.0% | 655.2ms |
| `eval_en_11` | EN | current_weather | What is the wind speed and cloud cover in Shi... | `get_current_weather, get_imd_alerts` | 100.0% | 737.1ms |
| `eval_en_12` | EN | forecast | Will it rain in Dibrugarh over the next 5 day... | `get_forecast, get_imd_alerts` | 100.0% | 715.67ms |
| `eval_en_13` | EN | imd_alerts | What color warning has IMD issued for East Kh... | `get_imd_alerts, get_current_weather` | 100.0% | 713.81ms |
| `eval_en_14` | EN | air_quality | Is the air pollution hazardous in Kolkata tod... | `get_air_quality, get_current_weather` | 100.0% | 1640.8ms |
| `eval_en_15` | EN | agromet | What is the recommended sowing weather for mu... | `get_agromet_advisory, get_current_weather` | 100.0% | 1572.05ms |
