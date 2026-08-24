"""Core WeatherGPT Agent Engine with hybrid function calling and deterministic Indic routing."""

import re
import time
from typing import Any, Dict, List, Optional, Tuple

from weathergpt.agent.multilingual import detect_language
from weathergpt.agent.tools import tool_registry
from weathergpt.core.models import (
    AgentToolCall,
    ChatRequest,
    ChatResponse,
    IMDAlert,
    LanguageCode,
)
from weathergpt.services.geocoding import INDIC_LOCATIONS_DATABASE


class WeatherAgentEngine:
    """Agent Engine orchestrating multilingual intent classification, tool-calling, and response synthesis."""

    def __init__(self):
        self.registry = tool_registry

    def _extract_location(self, text: str, fallback_hint: Optional[str] = None) -> str:
        """Extracts location name from message text or returns fallback."""
        lowered = text.lower()

        # Indic script city map with stem variations
        indic_city_map = {
            "ডিব্ৰুগড়": "Dibrugarh", "ডিব্ৰুগড়": "Dibrugarh", "dibrugarh": "Dibrugarh",
            "গুৱাহাটী": "Guwahati", "guwahati": "Guwahati",
            "শিলচৰ": "Silchar", "silchar": "Silchar",
            "যোৰহাট": "Jorhat", "jorhat": "Jorhat",
            "তেজপুৰ": "Tezpur", "tezpur": "Tezpur",
            "নগাঁও": "Nagaon", "nagaon": "Nagaon",
            "শিলং": "Shillong", "shillong": "Shillong",
            "আগরতলা": "Agartala", "আগৰতলা": "Agartala", "agartala": "Agartala",
            "ইম্ফল": "Imphal", "imphal": "Imphal",
            "কোহিমা": "Kohima", "kohima": "Kohima",
            "আইজল": "Aizawl", "aizawl": "Aizawl",
            "ইটানগৰ": "Itanagar", "itanagar": "Itanagar",
            "গেংটক": "Gangtok", "gangtok": "Gangtok",
            "दिल्ली": "New Delhi", "delhi": "New Delhi",
            "मुंबई": "Mumbai", "mumbai": "Mumbai",
            "कोलकाता": "Kolkata", "কলিকতা": "Kolkata", "kolkata": "Kolkata",
            "चेन्नई": "Chennai", "chennai": "Chennai",
            "बेंगलुरु": "Bengaluru", "bengaluru": "Bengaluru",
            "जयपुर": "Jaipur", "jaipur": "Jaipur",
            "लखनऊ": "Lucknow", "lucknow": "Lucknow",
            "पटना": "Patna", "patna": "Patna",
            "पुणे": "Pune", "pune": "Pune",
            "हैदराबाद": "Hyderabad", "hyderabad": "Hyderabad",
            "अहमदाबाद": "Ahmedabad", "ahmedabad": "Ahmedabad",
            "भोपाल": "Bhopal", "bhopal": "Bhopal",
            "चंडीगढ़": "Chandigarh", "chandigarh": "Chandigarh",
            "शिमला": "Shimla", "shimla": "Shimla",
            "श्रीनगर": "Srinagar", "srinagar": "Srinagar",
            "भुवनेश्वर": "Bhubaneswar", "bhubaneswar": "Bhubaneswar",
            "वाराणसी": "Varanasi", "varanasi": "Varanasi",
        }

        for k, v in indic_city_map.items():
            if k in lowered:
                return v

        # Check known Indic locations
        for loc_key, loc_obj in INDIC_LOCATIONS_DATABASE.items():
            if loc_key in lowered:
                return loc_obj.name

        # Check common city patterns
        match = re.search(r"(?:in|at|for|of|near|ৰ|ত|ৰ বাবে|में|का)\s+([A-Za-z\u0900-\u097F\u0980-\u09FF]+)", text)
        if match:
            extracted = match.group(1).strip()
            # Clean common postpositions / suffixes
            extracted = re.sub(r"[ৰততেমে]$", "", extracted)
            if len(extracted) > 2 and extracted.lower() not in ["weather", "forecast", "alert", "climate", "mausam", "botor", "বৰষুণ"]:
                return extracted

        if fallback_hint:
            return fallback_hint

        return "Guwahati"  # Default reference hub for WeatherGPT

    def _extract_crop(self, text: str) -> Optional[str]:
        """Extracts crop mention from user query."""
        lowered = text.lower()
        crops = {
            "rice": ["rice", "paddy", "ধান", "শালি ধান", "चावल", "धान"],
            "tea": ["tea", "চাহ", "चाय", "tea garden", "চাহ বাগিচা"],
            "mustard": ["mustard", "rapeseed", "সৰিয়হ", "सरसों", "तोरी"],
            "wheat": ["wheat", "গম", "गेहूं"],
            "jute": ["jute", "মৰাপাট", "पटसन"],
            "vegetables": ["vegetable", "tomato", "chili", "শাক-পাচলি", "सब्जी", "सब्जियां", "বিলাহী"],
        }
        for crop_id, variants in crops.items():
            if any(v in lowered for v in variants):
                return crop_id
        return None

    def _classify_intent_tools(self, message: str) -> List[Tuple[str, Dict[str, Any]]] :
        """Determines which meteorological tools need to be executed."""
        lowered = message.lower()
        loc = self._extract_location(message)
        crop = self._extract_crop(message)
        tool_invocations: List[Tuple[str, Dict[str, Any]]] = []

        # 1. Agricultural / Farmer Query
        if crop or any(w in lowered for w in ["farmer", "kisan", "krishi", "spray", "irrigation", "farming", "কৃষক", "পথাৰ", "শস্য", "খেতি", "ফসল", "सिंचाई"]):
            target_crop = crop or "rice"
            tool_invocations.append(("get_agromet_advisory", {"crop": target_crop, "location": loc}))
            tool_invocations.append(("get_current_weather", {"location": loc}))
            return tool_invocations

        # 2. Climate Science Q&A
        climate_triggers = [
            "monsoon", "southwest monsoon", "bordoisila", "kalbaishakhi", "western disturbance",
            "el nino", "la nina", "cyclone", "heatwave", "urban heat island", "iod", "enso",
            "মৌচুমী", "বৰদৈচিলা", "পশ্চিমীয়া ঝঞ্ঝা", "ঘূৰ্ণীবতাহ", "এল নিনো", "লা নিনা", "ডাইপোল",
            "উত্তাপ তৰংগ", "নগৰীয়া উত্তাপ",
            "मॉनसून", "चक्रवात", "लू", "कालवैशाखी", "पश्चिमी विक्षोभ", "एल नीनो", "ला नीना",
            "हीटवेव", "अर्बन हीट आइलैंड"
        ]
        if any(w in lowered for w in climate_triggers) and not any(w in lowered for w in ["today", "tomorrow", "current", "forecast", "आजी", "आज"]):
            tool_invocations.append(("search_climate_knowledge", {"query": message}))
            return tool_invocations

        # 3. IMD Alerts & Warnings
        if any(w in lowered for w in ["alert", "warning", "imd", "danger", "cyclone warning", "flood", "সতৰ্কবাৰ্তা", "বিপদ", "বানপানী", "चेतावनी", "अलर्ट"]):
            tool_invocations.append(("get_imd_alerts", {"location": loc}))
            tool_invocations.append(("get_current_weather", {"location": loc}))
            return tool_invocations

        # 4. Air Quality & Pollution
        if any(w in lowered for w in ["air quality", "aqi", "pollution", "pm2.5", "smog", "বায়ুৰ মান", "বায়ুৰ গুণমান", "প্ৰদূষণ", "वायु गुणवत्ता", "प्रदूषण"]):
            tool_invocations.append(("get_air_quality", {"location": loc}))
            tool_invocations.append(("get_current_weather", {"location": loc}))
            return tool_invocations

        # 5. GFS Numerical Physics
        if any(w in lowered for w in ["gfs", "cape", "convective", "shear", "numerical model", "soundings", "synoptic", "जीएफएस", "अस्थिरता", "অস্থিৰতা", "বায়ুমণ্ডলীয়"]):
            tool_invocations.append(("get_gfs_prediction", {"location": loc}))
            tool_invocations.append(("get_current_weather", {"location": loc}))
            return tool_invocations

        # 6. Multi-day Forecast
        forecast_terms = [
            "forecast", "tomorrow", "weekly", "next 7 days", "next 5 days", "next 3 days",
            "7-day", "5-day", "3-day", "7 day", "5 day", "3 day", "trend", "rain this week",
            "next few days", "coming days", "কাইলৈ", "সপ্তাহৰ বতৰ", "অহা", "দিনৰ বতৰ", "কালৈ",
            "कल का मौसम", "पूर्वानुमान", "आगामी", "अगले", "इस सप्ताह"
        ]
        if any(w in lowered for w in forecast_terms) or re.search(r"\d+[- ]day|next \d+ days|অহা \d+ দিন|अगले \d+ दिन", lowered):
            tool_invocations.append(("get_forecast", {"location": loc, "days": 7}))
            tool_invocations.append(("get_imd_alerts", {"location": loc}))
            return tool_invocations

        # 7. Default Current Weather + Alerts
        tool_invocations.append(("get_current_weather", {"location": loc}))
        tool_invocations.append(("get_imd_alerts", {"location": loc}))
        return tool_invocations

    def _synthesize_response(
        self,
        lang: LanguageCode,
        message: str,
        tool_results: List[AgentToolCall],
    ) -> Tuple[str, Optional[Dict[str, Any]], List[IMDAlert], Optional[Any]]:
        """Synthesizes structured, culturally aligned response based on tool outputs."""
        weather_summary = None
        alerts: List[IMDAlert] = []
        agromet = None
        sections: List[str] = []

        for call in tool_results:
            if not call.success or not call.result:
                continue

            if call.tool_name == "get_current_weather":
                weather_summary = call.result
                loc_data = call.result.get("location", {})
                curr = call.result.get("current", {})
                city = loc_data.get("name", "Target Location")
                temp = curr.get("temperature_c", "--")
                app_temp = curr.get("apparent_temperature_c", "--")
                hum = curr.get("relative_humidity_pct", "--")
                wind = curr.get("wind_speed_kmh", "--")
                rain = curr.get("precipitation_mm", 0.0)
                desc = curr.get("weather_desc", "Normal")

                if lang == LanguageCode.AS:
                    sections.append(
                        f"📍 **{city}ৰ বৰ্তমান বতৰৰ তথ্য:**\n"
                        f"• **উষ্ণতা:** {temp}°C (অনুভৱ হোৱা উষ্ণতা: {app_temp}°C)\n"
                        f"• **অৱস্থা:** {desc}\n"
                        f"• **আৰ্দ্ৰতা:** {hum}% | **বতাহৰ গতি:** {wind} কি.মি./ঘণ্টা\n"
                        f"• **বৰষুণ:** {rain} মি.মি."
                    )
                elif lang == LanguageCode.HI:
                    sections.append(
                        f"📍 **{city} में वर्तमान मौसम विवरण:**\n"
                        f"• **तापमान:** {temp}°C (महसूस होने वाला तापमान: {app_temp}°C)\n"
                        f"• **स्थिति:** {desc}\n"
                        f"• **आर्द्रता:** {hum}% | **हवा की गति:** {wind} किमी/घंटा\n"
                        f"• **वर्षा:** {rain} मिमी"
                    )
                else:
                    sections.append(
                        f"📍 **Current Weather in {city}:**\n"
                        f"• **Temperature:** {temp}°C (Feels like: {app_temp}°C)\n"
                        f"• **Condition:** {desc}\n"
                        f"• **Humidity:** {hum}% | **Wind Speed:** {wind} km/h\n"
                        f"• **Precipitation:** {rain} mm"
                    )

            elif call.tool_name == "get_forecast":
                weather_summary = call.result
                loc_data = call.result.get("location", {})
                daily = call.result.get("daily", [])
                city = loc_data.get("name", "Location")

                if daily:
                    if lang == LanguageCode.AS:
                        f_lines = [f"📅 **{city}ৰ ৭ দিনৰ বতৰৰ পূৰ্বানুমান:**"]
                        for d in daily[:5]:
                            f_lines.append(
                                f"• **{d.get('date')}:** {d.get('weather_desc')} | "
                                f"সৰ্বোচ্চ: {d.get('max_temp_c')}°C, সৰ্বনিম্ন: {d.get('min_temp_c')}°C | "
                                f"বৰষুণৰ সম্ভাৱনা: {d.get('precipitation_probability_pct')}%"
                            )
                        sections.append("\n".join(f_lines))
                    elif lang == LanguageCode.HI:
                        f_lines = [f"📅 **{city} के लिए आगामी मौसम पूर्वानुमान:**"]
                        for d in daily[:5]:
                            f_lines.append(
                                f"• **{d.get('date')}:** {d.get('weather_desc')} | "
                                f"अधिकतम: {d.get('max_temp_c')}°C, न्यूनतम: {d.get('min_temp_c')}°C | "
                                f"बारिश की संभावना: {d.get('precipitation_probability_pct')}%"
                            )
                        sections.append("\n".join(f_lines))
                    else:
                        f_lines = [f"📅 **7-Day Weather Forecast for {city}:**"]
                        for d in daily[:5]:
                            f_lines.append(
                                f"• **{d.get('date')}:** {d.get('weather_desc')} | "
                                f"High: {d.get('max_temp_c')}°C, Low: {d.get('min_temp_c')}°C | "
                                f"Rain Probability: {d.get('precipitation_probability_pct')}%"
                            )
                        sections.append("\n".join(f_lines))

            elif call.tool_name == "get_imd_alerts":
                alert_list = call.result
                if isinstance(alert_list, list):
                    for a_raw in alert_list:
                        try:
                            a_obj = IMDAlert(**a_raw)
                            alerts.append(a_obj)
                        except Exception:
                            pass

                if alerts:
                    active = [a for a in alerts if a.severity.value in ["Yellow", "Orange", "Red"]]
                    if active:
                        al = active[0]
                        color_badge = {"Yellow": "🟡", "Orange": "🟠", "Red": "🔴"}.get(al.severity.value, "⚠️")
                        if lang == LanguageCode.AS:
                            prec = "\n".join([f"  - {act}" for act in al.safety_actions_as[:3]])
                            sections.append(
                                f"{color_badge} **বতৰ বিজ্ঞান কেন্দ্ৰৰ সতৰ্কবাৰ্তা ({al.severity.value} Alert - {al.district}):**\n"
                                f"• **ঘটনাক্ৰম:** {al.event_type}\n"
                                f"• **বিৱৰণ:** {al.description}\n"
                                f"• **নিৰাপত্তা নিৰ্দেশনা:**\n{prec}"
                            )
                        elif lang == LanguageCode.HI:
                            prec = "\n".join([f"  - {act}" for act in al.safety_actions_hi[:3]])
                            sections.append(
                                f"{color_badge} **मौसम विभाग की चेतावनी ({al.severity.value} Alert - {al.district}):**\n"
                                f"• **प्रकार:** {al.event_type}\n"
                                f"• **विवरण:** {al.description}\n"
                                f"• **सुरक्षा निर्देश:**\n{prec}"
                            )
                        else:
                            prec = "\n".join([f"  - {act}" for act in al.safety_actions_en[:3]])
                            sections.append(
                                f"{color_badge} **IMD Weather Advisory ({al.severity.value} Alert - {al.district}):**\n"
                                f"• **Event:** {al.event_type}\n"
                                f"• **Summary:** {al.description}\n"
                                f"• **Actionable Precautions:**\n{prec}"
                            )

            elif call.tool_name == "get_air_quality":
                aq = call.result
                aqi = aq.get("aqi", 50)
                pm25 = aq.get("pm_2_5", aq.get("pm2_5", 25.0))
                pm10 = aq.get("pm10", 50.0)
                cat = aq.get("category", "Moderate")

                if lang == LanguageCode.AS:
                    advice = aq.get("health_advice_as", "")
                    sections.append(
                        f"🍃 **বায়ুৰ গুণমান সূচক (AQI) - {aq.get('location', {}).get('name')}:**\n"
                        f"• **AQI মান:** {aqi} ({cat})\n"
                        f"• **PM2.5:** {pm25} µg/m³ | **PM10:** {pm10} µg/m³\n"
                        f"• **স্বাস্থ্য পৰামৰ্শ:** {advice}"
                    )
                elif lang == LanguageCode.HI:
                    advice = aq.get("health_advice_hi", "")
                    sections.append(
                        f"🍃 **वायु गुणवत्ता सूचकांक (AQI) - {aq.get('location', {}).get('name')}:**\n"
                        f"• **AQI स्तर:** {aqi} ({cat})\n"
                        f"• **PM2.5:** {pm25} µg/m³ | **PM10:** {pm10} µg/m³\n"
                        f"• **स्वास्थ्य सलाह:** {advice}"
                    )
                else:
                    advice = aq.get("health_advice_en", "")
                    sections.append(
                        f"🍃 **Air Quality Index (AQI) - {aq.get('location', {}).get('name')}:**\n"
                        f"• **AQI Value:** {aqi} ({cat})\n"
                        f"• **PM2.5:** {pm25} µg/m³ | **PM10:** {pm10} µg/m³\n"
                        f"• **Health Recommendation:** {advice}"
                    )

            elif call.tool_name == "get_agromet_advisory":
                agromet = call.result
                crop_name = agromet.get("crop_name", "Crop")
                stage = agromet.get("growth_stage", "")
                irrig = agromet.get("irrigation_advice", "")
                fert = agromet.get("fertilizer_pesticide_advice", "")

                if lang == LanguageCode.AS:
                    adv = agromet.get("advisory_as", "")
                    sections.append(
                        f"🌾 **কৃষি বতৰ পৰামৰ্শ (গ্ৰামীণ কৃষি বতৰ সেৱা - {crop_name}):**\n"
                        f"• **শস্যৰ বৃদ্ধি অৱস্থা:** {stage}\n"
                        f"• **পৰামৰ্শ:** {adv}\n"
                        f"• **জলসিঞ্চন নিৰ্দেশনা:** {irrig}\n"
                        f"• **কীটনাশক/সাৰ প্ৰয়োগ:** {fert}"
                    )
                elif lang == LanguageCode.HI:
                    adv = agromet.get("advisory_hi", "")
                    sections.append(
                        f"🌾 **कृषि मौसम परामर्श (ग्रामीण कृषि मौसम सेवा - {crop_name}):**\n"
                        f"• **फसल की अवस्था:** {stage}\n"
                        f"• **मुख्य सलाह:** {adv}\n"
                        f"• **सिंचाई निर्देश:** {irrig}\n"
                        f"• **उर्वरक एवं कीटनाशक:** {fert}"
                    )
                else:
                    adv = agromet.get("advisory_en", "")
                    sections.append(
                        f"🌾 **Agro-Meteorological Advisory (GKMS - {crop_name}):**\n"
                        f"• **Crop Growth Stage:** {stage}\n"
                        f"• **Core Advisory:** {adv}\n"
                        f"• **Irrigation Directive:** {irrig}\n"
                        f"• **Fertilizer & Spray:** {fert}"
                    )

            elif call.tool_name == "get_gfs_prediction":
                gfs = call.result
                cape = gfs.get("cape_j_kg", 1200.0)
                pw = gfs.get("total_precipitable_water_kg_m2", 45.0)
                syn = gfs.get("synoptic_summary", "")

                if lang == LanguageCode.AS:
                    sections.append(
                        f"🌐 **NOAA GFS গাণিতিক বায়ুমণ্ডলীয় বিশ্লেষণ (০.২৫° ৰিজলিউচন):**\n"
                        f"• **CAPE (বায়ুমণ্ডলীয় অস্থিৰতা):** {cape} J/kg\n"
                        f"• **মুঠ জলীয় বাষ্প:** {pw} kg/m²\n"
                        f"• **বাৰ্তা:** {syn}"
                    )
                elif lang == LanguageCode.HI:
                    sections.append(
                        f"🌐 **NOAA GFS संख्यात्मक मौसम पूर्वानुमान (0.25° मॉडल):**\n"
                        f"• **CAPE (संवहनीय अस्थिरता):** {cape} J/kg\n"
                        f"• **कुल अवक्षेपण योग्य जल:** {pw} kg/m²\n"
                        f"• **सारांश:** {syn}"
                    )
                else:
                    sections.append(
                        f"🌐 **NOAA GFS Numerical Atmospheric Sounding (0.25° Resolution):**\n"
                        f"• **CAPE Instability:** {cape} J/kg\n"
                        f"• **Total Precipitable Water:** {pw} kg/m²\n"
                        f"• **Synoptic Summary:** {syn}"
                    )

            elif call.tool_name == "search_climate_knowledge":
                fact = call.result
                title = fact.get("title", "Climate Fact")
                if lang == LanguageCode.AS:
                    exp = fact.get("explanation_as", fact.get("explanation_en", ""))
                    sections.append(
                        f"📚 **জলবায়ু বিজ্ঞান তথ্যকোষ: {title}**\n"
                        f"{exp}\n\n"
                        f"🔬 *বৈজ্ঞানিক ভিত্তি:* {fact.get('scientific_basis', '')} (উৎস: {fact.get('source_agency', 'IMD')})"
                    )
                elif lang == LanguageCode.HI:
                    exp = fact.get("explanation_hi", fact.get("explanation_en", ""))
                    sections.append(
                        f"📚 **जलवायु विज्ञान ज्ञानकोष: {title}**\n"
                        f"{exp}\n\n"
                        f"🔬 *वैज्ञानिक आधार:* {fact.get('scientific_basis', '')} (स्रोत: {fact.get('source_agency', 'IMD')})"
                    )
                else:
                    exp = fact.get("explanation_en", "")
                    sections.append(
                        f"📚 **Climate Science Knowledge Base: {title}**\n"
                        f"{exp}\n\n"
                        f"🔬 *Scientific Basis:* {fact.get('scientific_basis', '')} (Source: {fact.get('source_agency', 'IMD')})"
                    )

        if not sections:
            if lang == LanguageCode.AS:
                reply = "নমস্কাৰ! মই WeatherGPT। আপোনাৰ অঞ্চলৰ বতৰৰ খবৰ, পূৰ্বানুমান, সতৰ্কবাৰ্তা বা কৃষি পৰামৰ্শ জানিবলৈ অনুগ্ৰহ কৰি সুধক।"
            elif lang == LanguageCode.HI:
                reply = "नमस्ते! मैं WeatherGPT हूँ। अपने शहर के मौसम, बारिश, वायु गुणवत्ता या फसलों की सलाह के लिए प्रश्न पूछें।"
            else:
                reply = "Hello! I am WeatherGPT. Ask me anything regarding live weather, forecasts, IMD alerts, air quality, or crop advisories."
        else:
            reply = "\n\n".join(sections)

        return reply, weather_summary, alerts, agromet

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Processes a chat query end-to-end with intent parsing, tool executions, and multilingual formatting."""
        start_time = time.perf_counter()

        # 1. Determine Language
        if request.language and request.language in ["en", "hi", "as"]:
            lang = LanguageCode(request.language)
        else:
            lang = detect_language(request.message)

        # 2. Classify required tools
        tool_plans = self._classify_intent_tools(request.message)

        # 3. Execute tools concurrently or sequentially
        executed_tool_calls: List[AgentToolCall] = []
        for tool_name, args in tool_plans:
            tool_call = await self.registry.execute_tool(tool_name, args)
            executed_tool_calls.append(tool_call)

        # 4. Synthesize final response
        reply, weather_summary, alerts, agromet = self._synthesize_response(
            lang=lang,
            message=request.message,
            tool_results=executed_tool_calls,
        )

        total_latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return ChatResponse(
            session_id=request.session_id or "default-session",
            reply=reply,
            detected_language=lang.value,
            tool_calls=executed_tool_calls,
            weather_summary=weather_summary,
            alerts=alerts,
            agromet=agromet,
            latency_ms=total_latency_ms,
            provider_used="WeatherGPT-Indic-Hybrid-Agent",
        )


weather_agent = WeatherAgentEngine()
