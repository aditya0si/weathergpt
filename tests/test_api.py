"""Integration tests for WeatherGPT FastAPI REST endpoints."""

import httpx
import pytest

from weathergpt.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "WeatherGPT"
        assert "as" in data["supported_languages"]
        assert data["active_tools_count"] >= 6


@pytest.mark.asyncio
async def test_languages_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/languages")
        assert resp.status_code == 200
        data = resp.json()
        codes = [lang["code"] for lang in data["languages"]]
        assert "en" in codes
        assert "hi" in codes
        assert "as" in codes


@pytest.mark.asyncio
async def test_chat_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "message": "Give me the weather forecast for Guwahati",
            "session_id": "test-session-001",
        }
        resp = await client.post("/api/v1/chat", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "test-session-001"
        assert len(data["reply"]) > 10
        assert len(data["tool_calls"]) >= 1


@pytest.mark.asyncio
async def test_weather_current_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/weather/current?location=Guwahati")
        assert resp.status_code == 200
        data = resp.json()
        assert data["location"]["name"] == "Guwahati"
        assert "temperature_c" in data["current"]


@pytest.mark.asyncio
async def test_weather_air_quality_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/weather/air-quality?location=Delhi")
        assert resp.status_code == 200
        data = resp.json()
        assert data["aqi"] > 0
        assert "category" in data


@pytest.mark.asyncio
async def test_agromet_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/agromet?crop=tea&location=Jorhat")
        assert resp.status_code == 200
        data = resp.json()
        assert "Tea" in data["crop_name"]
        assert len(data["advisory_as"]) > 0


@pytest.mark.asyncio
async def test_climate_kb_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/climate-kb?query=bordoisila")
        assert resp.status_code == 200
        data = resp.json()
        assert data["topic"] == "bordoisila"
