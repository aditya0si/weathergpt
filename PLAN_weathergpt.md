# PLAN_weathergpt.md — WeatherGPT Implementation Plan

## Section A — Goal & Acceptance Criteria

### Technical Restatement
WeatherGPT is an Indic multilingual conversational weather intelligence platform designed for SIH26068. It combines a function-calling LLM agent with real-time and numerical weather prediction (NWP) providers (Open-Meteo, India Meteorological Department [IMD] bulletins/alerts, and NOAA GFS models), an agricultural weather advisory engine, and a climate knowledge base. The system natively supports English, Hindi (`hi`), and Assamese (`as` — Northeast Indic language) with language auto-detection and culturally grounded response generation. It features a FastAPI high-performance backend, an interactive React + Vite glassmorphic chat dashboard with live forecast widgets and tool-execution inspection, a 50-question multilingual evaluation suite with latency and correctness scoring, and Hugging Face dataset/model card artifacts for Indic climate fine-tuning.

### Observable "Done" Definition
1. **Backend & Tool-Calling Agent**: FastAPI service starts cleanly with `/health` returning status 200, `/api/v1/chat` executing multi-step tool calling (e.g. `get_current_weather`, `get_forecast`, `get_imd_alerts`, `get_air_quality`, `get_agromet_advisory`, `search_climate_knowledge`), with streaming/non-streaming responses in English, Hindi, and Assamese.
2. **Deterministic & External LLM Modes**: Agent runs reliably without requiring paid external API keys using an intelligent built-in Indic Weather Agent router & parser, while seamlessly accepting OpenAI/Gemini/Groq/HuggingFace API keys via `.env` when present.
3. **Frontend UI**: Complete React 18+ Vite interface with Tailwind CSS, Lucide icons, interactive forecast charts (Recharts), AQI meters, severe alert notifications, language toggle, and agent tool execution inspection trays.
4. **Evaluation Benchmark**: `evals/run_evals.py` runs end-to-end against 50 multilingual test cases (`evals/data/weathergpt_eval_50.json`) measuring tool selection accuracy, answer correctness, language consistency, and latency (p50/p95), emitting markdown results to `evals/RESULTS.md` and README.
5. **Testing & CI**: Pytest suite covering core models, services, agent routing, and API endpoints with 100% passing tests (`pytest` exits code 0). GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs linting and test suite.
6. **Documentation & Release**: Comprehensive `README.md` with Mermaid architecture diagrams, quickstart instructions, API schema, benchmark tables, `LICENSE` (MIT), `.env.example`, `pyproject.toml`, and Git repository initialized with initial commit `feat: initial implementation`.

### Out of Scope
- Full-scale multi-GPU training cluster (replaced by working LoRA/PEFT fine-tuning script + small-model fallback + Hugging Face dataset cards).
- Direct Doppler radar binary decoding (IMD nowcast & radar summary alerts are integrated via structured JSON/bulletin parsers).

---

## Section B — Tech Stack & Constraints

### Stack Declarations
- **Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic v2, HTTPX, PyYAML, Python-dotenv.
- **Agent & Weather Services**: Custom asynchronous Tool Registry, Open-Meteo REST API, IMD Alert Feeds Parser, NOAA GFS Data Extractor, Indic Translation/Prompt Dispatcher.
- **Frontend**: React 18 / 19, TypeScript/JavaScript, Vite, Tailwind CSS, Lucide React, Recharts / Canvas Charting.
- **Evaluation & ML**: Pytest, Pytest-asyncio, Pandas/Numpy scoring harness, Hugging Face Hub dataset format (`datasets`/`transformers` compatible schemas).
- **CI / CD**: GitHub Actions (`.github/workflows/ci.yml`), Ruff/Flake8 linting.

### Architectural Decisions & Alternatives
- **LLM Agent Routing**:
  - *Chosen*: Hybrid Agent Engine supporting both Native LLM Function Calling (OpenAI/Gemini/Groq API) and an embedded rule-based / semantic pattern Indic agent fallback.
  - *Rejected — External-Only LLMs*: Would fail local tests and CI when API keys are not supplied.
  - *Rejected — Heavy Local Transformers in Dev Server*: Would require 10GB+ GPU memory and take minutes to initialize locally.
- **Multilingual Support**:
  - *Chosen*: Multilingual system prompts and prompt chaining with lexicon mapping for English, Hindi, and Assamese (`as`), ensuring low latency and high fidelity.
- **Weather Data Layer**:
  - *Chosen*: Open-Meteo (global + high-res India coverage) + IMD bulletin & warning alerts aggregator + GFS NWP model integration.

---

## Section C — Blocking Questions (0–3) & Assumptions

### Blocking Questions (0)
- `None (0)` — All core requirements are fully addressed with concrete defaults below.

### Falsifiable Assumptions
1. `[ASSUMPTION 1: Environment & Network]` The environment has Python 3.11+ and Node.js 18+ available. Network requests to public endpoints (Open-Meteo) may run during live mode, with resilient mocked fallbacks for isolated offline testing and CI.
2. `[ASSUMPTION 2: Fallback LLM Execution]` When no `OPENAI_API_KEY` or `GEMINI_API_KEY` is provided, the agent transparently falls back to the embedded deterministic Indic weather agent engine, ensuring 100% of test cases and evals execute without external dependencies.
3. `[ASSUMPTION 3: Target Languages]` The three primary languages are English (`en`), Hindi (`hi`), and Assamese (`as`) as the designated North-East Indic language, fully supported in the UI, system prompts, and the 50-pair evaluation dataset.
4. `[ASSUMPTION 4: Testing Scope]` Unit and integration tests cover all API routes, data connectors, weather tool parsers, agent reasoning steps, and multilingual evaluation metrics.

---

## Section D — Session Modularization

### Session 1: Project Scaffolding & Core Domain Models
- **Objective**: Establish clean repo structure, configuration system, domain models (Pydantic), and environment specifications.
- **Scope**: `pyproject.toml`, `requirements.txt`, `.env.example`, `LICENSE`, `src/weathergpt/core/config.py`, `src/weathergpt/core/models.py`.
- **Output**: Validated settings and data models with passing baseline unit tests.
- **Connects To**: Weather service adapters in Session 2.
- **Failure Surface**: Dependency conflicts or Pydantic validation errors.

### Session 2: Weather Data Adapters & Services
- **Objective**: Implement real data integrations for Open-Meteo, IMD alerts & bulletins parser, NOAA GFS extractor, Agro-meteorological advisory engine, and Climate Q&A knowledge engine.
- **Scope**: `src/weathergpt/services/openmeteo.py`, `src/weathergpt/services/imd.py`, `src/weathergpt/services/gfs.py`, `src/weathergpt/services/agromet.py`, `src/weathergpt/services/climate_kb.py`, `src/weathergpt/services/geocoding.py`.
- **Output**: Tested standalone weather tools capable of fetching current, forecast, air quality, agro advisories, and severe warnings for any Indian coordinates/city.
- **Connects To**: Agent tool registry in Session 3.
- **Failure Surface**: External API rate limits or schema changes (handled by fallback caching and resilient parsers).

### Session 3: Multilingual Tool-Calling Agent Engine & API
- **Objective**: Build the function-calling agent engine, multilingual prompt management (EN/HI/AS), tool execution dispatcher, and FastAPI REST endpoints.
- **Scope**: `src/weathergpt/agent/`, `src/weathergpt/api/`, `src/weathergpt/main.py`.
- **Output**: Fully functional REST server with `/health`, `/api/v1/chat`, `/api/v1/weather/*`, `/api/v1/agromet`, with full tool-calling traces.
- **Connects To**: Evaluation suite (Session 4) and Frontend UI (Session 5).
- **Failure Surface**: Agent tool-calling routing failure or serialization errors.

### Session 4: Evaluation Benchmark Suite & ML / Hugging Face Artifacts
- **Objective**: Build the 50-question Indic evaluation dataset, automated evaluation runner with latency/accuracy metrics, LoRA fine-tuning training script, and Hugging Face model/dataset cards.
- **Scope**: `evals/data/weathergpt_eval_50.json`, `evals/run_evals.py`, `scripts/train_indic_lora.py`, `artifacts/huggingface/MODEL_CARD.md`, `artifacts/huggingface/DATASET_CARD.md`.
- **Output**: Executable `python evals/run_evals.py` producing `evals/RESULTS.md` with complete metrics table.
- **Connects To**: Final documentation and test verification.
- **Failure Surface**: Benchmark timeout or scoring drift.

### Session 5: Modern React + Vite Dashboard & Chat UI
- **Objective**: Build the interactive frontend with dark/glassmorphic weather theme, live forecast widgets, AQI meters, severe alert notifications, tool execution inspector, and language switcher (EN/HI/AS).
- **Scope**: `frontend/` (Vite, React, Tailwind CSS, components, build configuration).
- **Output**: Fully buildable and testable frontend web application (`npm run build` succeeds).
- **Connects To**: End-to-end user workflow.
- **Failure Surface**: UI bundle build errors or responsive layout glitches.

### Session 6: CI/CD, Test Suite Verification, Documentation & Release
- **Objective**: Comprehensive pytest test suite, GitHub Actions CI workflow, complete README with Mermaid architecture diagrams, and initial Git commit.
- **Scope**: `tests/`, `.github/workflows/ci.yml`, `README.md`, Git commit.
- **Output**: 100% passing tests, verified clean repository state, and final summary report.
- **Connects To**: Final project completion.

---

## Section E — Progress Checklist

- [ ] Session 1: Project Scaffolding & Core Domain Models
  - [ ] Initialize `pyproject.toml`, `requirements.txt`, `.env.example`, `LICENSE` (MIT)
  - [ ] Create `src/weathergpt/core/` configuration and Pydantic schemas
  - [ ] Write unit tests for core configuration and schemas
- [ ] Session 2: Weather Data Adapters & Services
  - [ ] Implement Open-Meteo adapter (current, hourly/daily forecast, air quality)
  - [ ] Implement IMD warning alerts & bulletin parser
  - [ ] Implement NOAA GFS numerical model adapter
  - [ ] Implement AgroMet farmer advisory engine & Climate Knowledge Base
  - [ ] Write unit tests for all weather data services
- [ ] Session 3: Multilingual Tool-Calling Agent Engine & FastAPI
  - [ ] Implement tool registry and function-calling agent engine
  - [ ] Implement Indic multilingual support (English, Hindi, Assamese)
  - [ ] Implement FastAPI endpoints (`/health`, `/api/v1/chat`, `/api/v1/weather/*`, `/api/v1/agromet`)
  - [ ] Write unit and integration tests for API and agent flows
- [ ] Session 4: Evaluation Benchmark Suite & ML / HF Artifacts
  - [ ] Create 50-question Indic benchmark dataset (`evals/data/weathergpt_eval_50.json`)
  - [ ] Implement evaluation harness (`evals/run_evals.py`) scoring latency, correctness, tool accuracy
  - [ ] Create Indic LoRA fine-tuning script (`scripts/train_indic_lora.py`) & HF model/dataset cards
- [ ] Session 5: Modern React + Vite Dashboard & Chat UI
  - [ ] Scaffold React + Vite + Tailwind CSS frontend in `frontend/`
  - [ ] Build Weather Chat, Forecast widgets, AQI gauge, Alert banners, Tool Inspection tray
  - [ ] Verify `npm run build` static generation
- [ ] Session 6: CI/CD, Documentation & Release
  - [ ] Configure `.github/workflows/ci.yml`
  - [ ] Write comprehensive `README.md` with Mermaid diagrams, setup, benchmarks, roadmap
  - [ ] Run full pytest suite (must exit 0) and evals runner
  - [ ] Git init & initial commit with message `feat: initial implementation`
