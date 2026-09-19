"""Unit and integration tests for WeatherGPT data services."""

import httpx
import pytest

from weathergpt.core.models import AlertSeverity, GeoLocation
from weathergpt.services.agromet import agromet_service
from weathergpt.services.climate_kb import climate_kb_service
from weathergpt.services.geocoding import geocoding_service
from weathergpt.services.gfs import gfs_service
from weathergpt.services.imd import imd_service
from weathergpt.services.openmeteo import decode_wmo_code, openmeteo_service


@pytest.mark.asyncio
async def test_geocoding_service_known_locations():
    loc = await geocoding_service.resolve_location("Guwahati")
    assert loc.name == "Guwahati"
    assert loc.admin1 == "Assam"
    assert round(loc.latitude, 2) == 26.14
    assert round(loc.longitude, 2) == 91.74


@pytest.mark.asyncio
async def test_geocoding_service_indic_script():
    loc = await geocoding_service.resolve_location("গুৱাহাটী")
    assert loc.name == "Guwahati"

    loc_delhi = await geocoding_service.resolve_location("दिल्ली")
    assert "Delhi" in loc_delhi.name


@pytest.mark.asyncio
async def test_openmeteo_service_forecast():
    loc = GeoLocation(
        name="Dibrugarh",
        latitude=27.4728,
        longitude=94.9120,
        admin1="Assam",
    )
    forecast = await openmeteo_service.get_forecast(loc)
    assert forecast.location.name == "Dibrugarh"
    assert forecast.current.temperature_c > -50.0
    assert len(forecast.daily) == 7
    assert len(forecast.hourly_summary) > 0


@pytest.mark.asyncio
async def test_openmeteo_service_air_quality():
    loc = GeoLocation(
        name="New Delhi",
        latitude=28.6139,
        longitude=77.2090,
        admin1="Delhi",
    )
    aqi = await openmeteo_service.get_air_quality(loc)
    assert aqi.aqi > 0
    assert aqi.pm2_5 > 0
    assert aqi.category in ["Good", "Moderate", "Poor", "Very Poor", "Severe"]


def test_wmo_weather_decoding():
    desc_en, cat = decode_wmo_code(0, "en")
    assert desc_en == "Clear sky"

    desc_hi, _ = decode_wmo_code(65, "hi")
    assert "भारी बारिश" in desc_hi

    desc_as, _ = decode_wmo_code(95, "as")
    assert "বজ্ৰপাত" in desc_as


@pytest.mark.asyncio
async def test_imd_alert_service():
    loc = GeoLocation(
        name="Guwahati",
        latitude=26.1445,
        longitude=91.7362,
        admin1="Assam",
        admin2="Kamrup Metropolitan",
    )
    alerts = await imd_service.get_alerts_for_location(loc)
    assert len(alerts) >= 1
    assert any(a.severity in [AlertSeverity.ORANGE, AlertSeverity.YELLOW, AlertSeverity.GREEN] for a in alerts)
    assert len(alerts[0].safety_actions_en) > 0
    assert len(alerts[0].safety_actions_as) > 0


@pytest.mark.asyncio
async def test_gfs_service():
    loc = GeoLocation(
        name="Kolkata",
        latitude=22.5726,
        longitude=88.3639,
        admin1="West Bengal",
    )
    gfs = await gfs_service.get_gfs_prediction(loc)
    assert gfs.cape_j_kg >= 0.0
    assert gfs.total_precipitable_water_kg_m2 > 0.0
    assert len(gfs.synoptic_summary) > 10


def test_agromet_service():
    loc = GeoLocation(
        name="Jorhat",
        latitude=26.7509,
        longitude=94.2037,
        admin1="Assam",
    )
    advisory = agromet_service.get_advisory_for_crop("rice", loc)
    assert "Paddy" in advisory.crop_name
    assert len(advisory.advisory_en) > 0
    assert len(advisory.advisory_as) > 0


def test_climate_kb_service():
    fact = climate_kb_service.search_climate_knowledge("Tell me about Bordoisila in Assam")
    assert fact is not None
    assert fact.topic == "bordoisila"
    assert "মাকৰ ঘৰলৈ" in fact.explanation_as

    wd_fact = climate_kb_service.search_climate_knowledge("Western Disturbance winter rains")
    assert wd_fact is not None
    assert wd_fact.topic == "western_disturbance"


@pytest.mark.asyncio
async def test_openmeteo_fallback_is_labelled_synthetic(monkeypatch):
    """Fabricated fallback data must never be presented as a live measurement."""

    async def _upstream_down(*args, **kwargs):
        raise httpx.ConnectError("simulated upstream outage")

    monkeypatch.setattr(httpx.AsyncClient, "get", _upstream_down)

    loc = GeoLocation(name="Dibrugarh", latitude=27.4728, longitude=94.9120, admin1="Assam")
    forecast = await openmeteo_service.get_forecast(loc)
    assert "synthetic" in forecast.source.lower()
    assert "live" not in forecast.source.lower()

    aqi = await openmeteo_service.get_air_quality(loc)
    assert "synthetic" in aqi.source.lower()
    assert "live" not in aqi.source.lower()


@pytest.mark.asyncio
async def test_imd_alerts_are_labelled_as_static_reference_data():
    """The shipped bulletins are a static reference set, not a live IMD feed."""
    loc = GeoLocation(
        name="Guwahati",
        latitude=26.1445,
        longitude=91.7362,
        admin1="Assam",
        admin2="Kamrup Metropolitan",
    )
    alerts = await imd_service.get_alerts_for_location(loc)
    assert len(alerts) >= 1
    for alert in alerts:
        assert "static reference" in alert.source.lower()
        # The payload must not attribute the bulletin to IMD as a live source.
        assert "india meteorological department" not in alert.source.lower()


@pytest.mark.asyncio
async def test_gfs_output_is_labelled_as_an_analytic_estimate():
    """GFS indices are computed analytically, not read from a NOAA model run."""
    loc = GeoLocation(name="Kolkata", latitude=22.5726, longitude=88.3639, admin1="West Bengal")
    gfs = await gfs_service.get_gfs_prediction(loc)
    assert "analytic" in gfs.source.lower()
    assert "not noaa gfs model output" in gfs.source.lower()
