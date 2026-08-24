"""Application configuration management for WeatherGPT."""

from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App Info
    app_name: str = "WeatherGPT"
    app_version: str = "1.0.0"
    app_description: str = (
        "Indic Multilingual Conversational AI Weather Platform (IMD / Open-Meteo / GFS)"
    )

    # Server settings
    weathergpt_host: str = "0.0.0.0"
    weathergpt_port: int = 8000
    weathergpt_debug: bool = False
    weathergpt_log_level: str = "INFO"

    # Multilingual settings (English, Hindi, Assamese)
    supported_languages: List[str] = ["en", "hi", "as"]
    weathergpt_default_language: Literal["en", "hi", "as"] = "en"

    # LLM Settings
    weathergpt_llm_provider: str = "hybrid"  # "hybrid", "openai", "gemini", "groq", "mock"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    gemini_model: str = "gemini-1.5-flash"
    groq_model: str = "llama-3.1-70b-versatile"

    # Remote API endpoints
    openmeteo_base_url: str = "https://api.open-meteo.com/v1"
    openmeteo_geocoding_url: str = "https://geocoding-api.open-meteo.com/v1"
    openmeteo_air_quality_url: str = "https://air-quality-api.open-meteo.com/v1"
    imd_bulletin_rss_url: str = "https://mausam.imd.gov.in/responsive/all_india_bulletin.php"
    imd_warning_url: str = "https://internal.imd.gov.in/pages/press_release_mausam.php"
    noaa_gfs_url: str = "https://nomads.ncep.noaa.gov/dods/gfs_0p25"

    # Resiliency & Performance
    cache_ttl_seconds: int = 300
    request_timeout_seconds: float = 10.0
    mock_network_fallback: bool = True


settings = Settings()
