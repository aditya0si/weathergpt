"""Unit tests for WeatherGPT Agent reasoning and multilingual parsing."""

import pytest

from weathergpt.agent.engine import weather_agent
from weathergpt.agent.multilingual import detect_language
from weathergpt.agent.prompts import get_system_prompt
from weathergpt.agent.tools import AGENT_TOOL_DEFINITIONS
from weathergpt.core.models import ChatRequest, LanguageCode


def test_agent_tool_definitions():
    assert len(AGENT_TOOL_DEFINITIONS) >= 6
    names = [t["function"]["name"] for t in AGENT_TOOL_DEFINITIONS]
    assert "get_current_weather" in names
    assert "get_forecast" in names
    assert "get_air_quality" in names
    assert "get_imd_alerts" in names
    assert "get_agromet_advisory" in names
    assert "search_climate_knowledge" in names


def test_language_detection():
    assert detect_language("What is the weather in Guwahati today?") == LanguageCode.EN
    assert detect_language("आज दिल्ली में बारिश होगी क्या?") == LanguageCode.HI
    assert detect_language("কাইলৈ গুৱাহাটীত বৰষুণ হবনে?") == LanguageCode.AS
    assert detect_language("অসমৰ বানপানীৰ পৰিস্থিতি কেনেকুৱা?") == LanguageCode.AS
    assert detect_language("कल मुंबई में मौसम कैसा रहेगा?") == LanguageCode.HI


def test_system_prompts():
    en_prompt = get_system_prompt(LanguageCode.EN)
    assert "WeatherGPT" in en_prompt
    assert "Celsius" in en_prompt

    hi_prompt = get_system_prompt(LanguageCode.HI)
    assert "WeatherGPT" in hi_prompt
    assert "सेल्सियस" in hi_prompt

    as_prompt = get_system_prompt(LanguageCode.AS)
    assert "WeatherGPT" in as_prompt
    assert "চেলছিয়াছ" in as_prompt


@pytest.mark.asyncio
async def test_agent_chat_english_weather():
    req = ChatRequest(message="What is the weather in Guwahati today?")
    resp = await weather_agent.chat(req)
    assert resp.detected_language == "en"
    assert "Guwahati" in resp.reply
    assert len(resp.tool_calls) >= 1
    assert resp.latency_ms > 0


@pytest.mark.asyncio
async def test_agent_chat_assamese_weather():
    req = ChatRequest(message="কাইলৈ ডিব্ৰুগড়ত বৰষুণ হবনে?")
    resp = await weather_agent.chat(req)
    assert resp.detected_language == "as"
    assert "ডিব্ৰুগড়" in resp.reply or "Dibrugarh" in resp.reply
    assert len(resp.tool_calls) >= 1


@pytest.mark.asyncio
async def test_agent_chat_hindi_agromet():
    req = ChatRequest(message="धान की फसल में सिंचाई की क्या सलाह है लखनऊ के लिए?")
    resp = await weather_agent.chat(req)
    assert resp.detected_language == "hi"
    assert "धान" in resp.reply or "Paddy" in resp.reply
    assert resp.agromet is not None


@pytest.mark.asyncio
async def test_agent_chat_climate_science():
    req = ChatRequest(message="Explain what is Bordoisila in Assam")
    resp = await weather_agent.chat(req)
    assert "Bordoisila" in resp.reply
    assert any(c.tool_name == "search_climate_knowledge" for c in resp.tool_calls)
