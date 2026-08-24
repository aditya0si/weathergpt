"""Core domain and data exchange models for WeatherGPT."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def _get_utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class LanguageCode(str, Enum):
    EN = "en"
    HI = "hi"
    AS = "as"


class AlertSeverity(str, Enum):
    GREEN = "Green"      # No warning
    YELLOW = "Yellow"    # Watch / Be updated
    ORANGE = "Orange"    # Alert / Be prepared
    RED = "Red"          # Warning / Take action


class WeatherConditionCategory(str, Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    SNOW = "snow"
    FOG = "fog"
    EXTREME = "extreme"


class GeoLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str = "India"
    admin1: Optional[str] = None  # State / Province
    admin2: Optional[str] = None  # District
    timezone: str = "Asia/Kolkata"
    elevation: Optional[float] = None
    population: Optional[int] = None


class CurrentWeather(BaseModel):
    temperature_c: float
    apparent_temperature_c: float
    relative_humidity_pct: int
    precipitation_mm: float
    wind_speed_kmh: float
    wind_direction_deg: float
    weather_code: int
    weather_desc: str
    condition_category: WeatherConditionCategory = WeatherConditionCategory.CLEAR
    surface_pressure_hpa: float = 1013.25
    cloud_cover_pct: int = 0
    uv_index: float = 0.0
    is_day: bool = True
    timestamp: str = Field(default_factory=_get_utc_now_iso)


class DailyForecastItem(BaseModel):
    date: str
    max_temp_c: float
    min_temp_c: float
    precipitation_sum_mm: float
    precipitation_probability_pct: int
    weather_code: int
    weather_desc: str
    condition_category: WeatherConditionCategory = WeatherConditionCategory.CLEAR
    max_wind_speed_kmh: float
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    uv_index_max: Optional[float] = None


class HourlyForecastItem(BaseModel):
    time: str
    temperature_c: float
    relative_humidity_pct: int
    precipitation_mm: float
    weather_code: int
    weather_desc: str
    wind_speed_kmh: float


class WeatherForecastResponse(BaseModel):
    location: GeoLocation
    current: CurrentWeather
    daily: List[DailyForecastItem]
    hourly_summary: List[HourlyForecastItem] = []
    source: str = "Open-Meteo & IMD Harmonized"
    generated_at: str = Field(default_factory=_get_utc_now_iso)


class AirQualityData(BaseModel):
    aqi: int
    pm2_5: float
    pm10: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float
    carbon_monoxide: float
    category: str  # Good, Satisfactory, Moderate, Poor, Very Poor, Severe
    health_advice_en: str
    health_advice_hi: str
    health_advice_as: str
    location: GeoLocation
    timestamp: str = Field(default_factory=_get_utc_now_iso)


class IMDAlert(BaseModel):
    alert_id: str
    district: str
    state: str
    severity: AlertSeverity
    event_type: str  # e.g. "Heavy Rainfall", "Thunderstorm & Lightning", "Heat Wave"
    description: str
    valid_from: str
    valid_to: str
    source: str = "India Meteorological Department (IMD)"
    safety_actions_en: List[str]
    safety_actions_hi: List[str]
    safety_actions_as: List[str]


class GFSModelPrediction(BaseModel):
    run_timestamp: str
    valid_timestamp: str
    latitude: float
    longitude: float
    cape_j_kg: float  # Convective Available Potential Energy
    total_precipitable_water_kg_m2: float
    wind_shear_0_6km_m_s: float
    simulated_reflectivity_dbz: float
    cyclone_genesis_index: float  # Scale 0.0 to 10.0
    synoptic_summary: str


class CropAgroAdvisory(BaseModel):
    crop_name: str
    growth_stage: str
    state: str
    district: Optional[str] = None
    advisory_en: str
    advisory_hi: str
    advisory_as: str
    irrigation_advice: str
    fertilizer_pesticide_advice: str
    harvesting_weather_window: str


class ClimateKnowledgeFact(BaseModel):
    topic: str
    keywords: List[str]
    title: str
    explanation_en: str
    explanation_hi: str
    explanation_as: str
    scientific_basis: str
    source_agency: str = "IMD / IPCC / MoES"


class AgentToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Any
    latency_ms: float
    success: bool = True
    error_message: Optional[str] = None


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system", "tool"
    content: str
    language: Optional[LanguageCode] = None
    tool_calls: Optional[List[AgentToolCall]] = None
    timestamp: str = Field(default_factory=_get_utc_now_iso)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    language: Optional[str] = None  # None for auto-detect, or "en", "hi", "as"
    location_hint: Optional[str] = None
    context_history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    detected_language: str
    tool_calls: List[AgentToolCall] = []
    weather_summary: Optional[Dict[str, Any]] = None
    alerts: List[IMDAlert] = []
    agromet: Optional[CropAgroAdvisory] = None
    latency_ms: float
    provider_used: str
