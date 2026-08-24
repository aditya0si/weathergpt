"""Agent Tool Registry and Execution Engine for WeatherGPT."""

import time
from typing import Any, Dict

from weathergpt.core.logger import logger
from weathergpt.core.models import AgentToolCall
from weathergpt.services.agromet import agromet_service
from weathergpt.services.climate_kb import climate_kb_service
from weathergpt.services.geocoding import geocoding_service
from weathergpt.services.gfs import gfs_service
from weathergpt.services.imd import imd_service
from weathergpt.services.openmeteo import openmeteo_service

# Tool Definitions for OpenAI / Gemini / Function-calling schemas
AGENT_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Fetch real-time current weather metrics (temperature, humidity, rain, wind, WMO condition) for any Indian city or district.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Name of the city, district, or region in India (e.g. 'Guwahati', 'Delhi', 'Dibrugarh').",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Fetch 7-day multi-day and hourly weather forecast with rain probabilities, max/min temperatures, and conditions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Target city, district, or state.",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of forecast days (1 to 7).",
                        "default": 7,
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_air_quality",
            "description": "Fetch Air Quality Index (AQI) and pollutant concentrations (PM2.5, PM10, NO2, SO2, CO) with health advisories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Target city or location.",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_imd_alerts",
            "description": "Fetch official India Meteorological Department (IMD) color-coded severe weather warnings (Green, Yellow, Orange, Red) and safety advisories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "District, city, or state name in India.",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_gfs_prediction",
            "description": "Query NOAA GFS numerical weather prediction model for atmospheric instability (CAPE), precipitable water, and synoptic conditions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to extract atmospheric sounding indices.",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_agromet_advisory",
            "description": "Fetch Gramin Krishi Mausam Sewa (GKMS) crop-specific agricultural weather advisory (paddy, tea, mustard, wheat, jute, vegetables) with irrigation and spray advice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "crop": {
                        "type": "string",
                        "description": "Crop name (e.g. 'rice', 'paddy', 'tea', 'mustard', 'wheat', 'jute', 'vegetables').",
                    },
                    "location": {
                        "type": "string",
                        "description": "Target agricultural location or district.",
                    },
                },
                "required": ["crop", "location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_climate_knowledge",
            "description": "Search verified meteorological knowledge and scientific explanations for Indian phenomena (Monsoon, Bordoisila, Kalbaishakhi, Western Disturbances, El Niño, Cyclones, Heatwaves).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Meteorological topic or climate question.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


class ToolRegistry:
    """Dispatches tool executions asynchronously with latency measurement."""

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> AgentToolCall:
        start_time = time.perf_counter()
        try:
            if tool_name == "get_current_weather":
                loc_name = arguments.get("location", "Guwahati")
                loc = await geocoding_service.resolve_location(loc_name)
                forecast = await openmeteo_service.get_forecast(loc)
                res = {
                    "location": loc.model_dump(),
                    "current": forecast.current.model_dump(),
                    "source": forecast.source,
                }
            elif tool_name == "get_forecast":
                loc_name = arguments.get("location", "Guwahati")
                loc = await geocoding_service.resolve_location(loc_name)
                forecast = await openmeteo_service.get_forecast(loc)
                res = forecast.model_dump()
            elif tool_name == "get_air_quality":
                loc_name = arguments.get("location", "New Delhi")
                loc = await geocoding_service.resolve_location(loc_name)
                aqi = await openmeteo_service.get_air_quality(loc)
                res = aqi.model_dump()
            elif tool_name == "get_imd_alerts":
                loc_name = arguments.get("location", "Guwahati")
                loc = await geocoding_service.resolve_location(loc_name)
                alerts = await imd_service.get_alerts_for_location(loc)
                res = [a.model_dump() for a in alerts]
            elif tool_name == "get_gfs_prediction":
                loc_name = arguments.get("location", "Kolkata")
                loc = await geocoding_service.resolve_location(loc_name)
                gfs = await gfs_service.get_gfs_prediction(loc)
                res = gfs.model_dump()
            elif tool_name == "get_agromet_advisory":
                crop = arguments.get("crop", "rice")
                loc_name = arguments.get("location", "Guwahati")
                loc = await geocoding_service.resolve_location(loc_name)
                forecast = await openmeteo_service.get_forecast(loc)
                advisory = agromet_service.get_advisory_for_crop(crop, loc, forecast)
                res = advisory.model_dump()
            elif tool_name == "search_climate_knowledge":
                query = arguments.get("query", "monsoon")
                fact = climate_kb_service.search_climate_knowledge(query)
                res = fact.model_dump() if fact else {"topic": "unknown", "explanation_en": "No specific record found."}
            else:
                raise ValueError(f"Unknown tool name: '{tool_name}'")

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return AgentToolCall(
                tool_name=tool_name,
                arguments=arguments,
                result=res,
                latency_ms=latency_ms,
                success=True,
            )
        except Exception as e:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(f"Error executing tool '{tool_name}': {e}")
            return AgentToolCall(
                tool_name=tool_name,
                arguments=arguments,
                result=None,
                latency_ms=latency_ms,
                success=False,
                error_message=str(e),
            )


tool_registry = ToolRegistry()
