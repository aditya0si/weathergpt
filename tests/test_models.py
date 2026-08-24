"""Unit tests for WeatherGPT core models."""

from weathergpt.core.models import (
    AlertSeverity,
    CurrentWeather,
    GeoLocation,
    IMDAlert,
    WeatherConditionCategory,
)


def test_geolocation_model():
    loc = GeoLocation(
        name="Guwahati",
        latitude=26.1445,
        longitude=91.7362,
        country="India",
        admin1="Assam",
    )
    assert loc.name == "Guwahati"
    assert loc.latitude == 26.1445
    assert loc.admin1 == "Assam"


def test_current_weather_model():
    cw = CurrentWeather(
        temperature_c=28.5,
        apparent_temperature_c=31.2,
        relative_humidity_pct=78,
        precipitation_mm=0.0,
        wind_speed_kmh=12.4,
        wind_direction_deg=180.0,
        weather_code=1,
        weather_desc="Mainly Clear",
        condition_category=WeatherConditionCategory.CLEAR,
    )
    assert cw.temperature_c == 28.5
    assert cw.is_day is True


def test_imd_alert_model():
    alert = IMDAlert(
        alert_id="IMD-AS-20260824-01",
        district="Kamrup Metropolitan",
        state="Assam",
        severity=AlertSeverity.ORANGE,
        event_type="Heavy Rainfall & Thunderstorm",
        description="Isolated heavy to very heavy rainfall expected over Kamrup Metropolitan.",
        valid_from="2026-08-24T00:00:00Z",
        valid_to="2026-08-25T00:00:00Z",
        safety_actions_en=["Stay indoors during lightning", "Avoid waterlogged roads"],
        safety_actions_hi=["बिजली चमकने के दौरान घर के अंदर रहें", "जलभराव वाले रास्तों से बचें"],
        safety_actions_as=["বজ্ৰপাতৰ সময়ত ঘৰৰ ভিতৰত থাকক", "পানী জমা হোৱা পথ পৰিহাৰ কৰক"],
    )
    assert alert.severity == AlertSeverity.ORANGE
    assert len(alert.safety_actions_as) == 2
