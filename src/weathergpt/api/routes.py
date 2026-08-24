"""FastAPI route handlers for WeatherGPT."""

from typing import List

from fastapi import APIRouter, HTTPException, Query

from weathergpt.agent.engine import weather_agent
from weathergpt.agent.tools import AGENT_TOOL_DEFINITIONS
from weathergpt.api.schemas import HealthResponse, LanguageInfo, LanguagesResponse
from weathergpt.core.config import settings
from weathergpt.core.models import (
    AirQualityData,
    ChatRequest,
    ChatResponse,
    CropAgroAdvisory,
    GFSModelPrediction,
    IMDAlert,
    WeatherForecastResponse,
)
from weathergpt.services.agromet import agromet_service
from weathergpt.services.climate_kb import climate_kb_service
from weathergpt.services.geocoding import geocoding_service
from weathergpt.services.gfs import gfs_service
from weathergpt.services.imd import imd_service
from weathergpt.services.openmeteo import openmeteo_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """System health check and operational status."""
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        service=settings.app_name,
        supported_languages=settings.supported_languages,
        active_tools_count=len(AGENT_TOOL_DEFINITIONS),
        llm_provider=settings.weathergpt_llm_provider,
    )


@router.get("/api/v1/languages", response_model=LanguagesResponse, tags=["Multilingual"])
async def list_languages():
    """Returns list of supported Indic languages and metadata."""
    return LanguagesResponse(
        languages=[
            LanguageInfo(code="en", name="English", native_name="English", region="Pan-India / Global"),
            LanguageInfo(code="hi", name="Hindi", native_name="हिन्दी", region="North & Central India"),
            LanguageInfo(code="as", name="Assamese", native_name="অসমীয়া", region="Northeast India (Assam & Brahmaputra Valley)"),
        ]
    )


@router.post("/api/v1/chat", response_model=ChatResponse, tags=["Conversational Agent"])
async def chat_endpoint(request: ChatRequest):
    """Conversational weather intelligence agent with multi-step tool calling and Indic generation."""
    try:
        return await weather_agent.chat(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@router.get("/api/v1/weather/current", response_model=WeatherForecastResponse, tags=["Weather Data"])
async def get_current_weather_endpoint(location: str = Query("Guwahati", description="City or district name")):
    """Get current meteorological metrics for a location."""
    loc = await geocoding_service.resolve_location(location)
    return await openmeteo_service.get_forecast(loc)


@router.get("/api/v1/weather/forecast", response_model=WeatherForecastResponse, tags=["Weather Data"])
async def get_forecast_endpoint(
    location: str = Query("Guwahati", description="City or district name"),
    days: int = Query(7, ge=1, le=7, description="Forecast days"),
):
    """Get 7-day weather forecast with daily and hourly breakdowns."""
    loc = await geocoding_service.resolve_location(location)
    return await openmeteo_service.get_forecast(loc)


@router.get("/api/v1/weather/air-quality", response_model=AirQualityData, tags=["Weather Data"])
async def get_air_quality_endpoint(location: str = Query("New Delhi", description="City or district name")):
    """Get Air Quality Index and pollutant concentrations."""
    loc = await geocoding_service.resolve_location(location)
    return await openmeteo_service.get_air_quality(loc)


@router.get("/api/v1/weather/alerts", response_model=List[IMDAlert], tags=["Severe Weather"])
async def get_imd_alerts_endpoint(location: str = Query("Guwahati", description="City or district name")):
    """Get official IMD warning bulletins and safety precautions."""
    loc = await geocoding_service.resolve_location(location)
    return await imd_service.get_alerts_for_location(loc)


@router.get("/api/v1/weather/gfs", response_model=GFSModelPrediction, tags=["Numerical Prediction"])
async def get_gfs_endpoint(location: str = Query("Kolkata", description="City or district name")):
    """Get NOAA GFS 0.25-degree numerical atmospheric instability metrics."""
    loc = await geocoding_service.resolve_location(location)
    return await gfs_service.get_gfs_prediction(loc)


@router.get("/api/v1/agromet", response_model=CropAgroAdvisory, tags=["Agriculture"])
async def get_agromet_endpoint(
    crop: str = Query("rice", description="Crop name (rice, tea, mustard, wheat, jute, vegetables)"),
    location: str = Query("Guwahati", description="Agricultural hub or district"),
):
    """Get Gramin Krishi Mausam Sewa (GKMS) farmer advisory."""
    loc = await geocoding_service.resolve_location(location)
    forecast = await openmeteo_service.get_forecast(loc)
    return agromet_service.get_advisory_for_crop(crop, loc, forecast)


@router.get("/api/v1/climate-kb", tags=["Climate Knowledge"])
async def get_climate_kb_endpoint(query: str = Query("monsoon", description="Meteorological term or question")):
    """Search verified climate science knowledge base."""
    fact = climate_kb_service.search_climate_knowledge(query)
    if not fact:
        raise HTTPException(status_code=404, detail="Climate topic not found in registry")
    return fact.model_dump()
