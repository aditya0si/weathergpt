"""Unit tests for WeatherGPT configuration."""

from weathergpt.core.config import Settings, settings


def test_default_settings():
    assert settings.app_name == "WeatherGPT"
    assert "en" in settings.supported_languages
    assert "hi" in settings.supported_languages
    assert "as" in settings.supported_languages
    assert settings.cache_ttl_seconds > 0
    assert settings.request_timeout_seconds > 0


def test_custom_settings():
    custom = Settings(
        weathergpt_port=9000,
        weathergpt_default_language="hi",
        weathergpt_debug=True,
    )
    assert custom.weathergpt_port == 9000
    assert custom.weathergpt_default_language == "hi"
    assert custom.weathergpt_debug is True
