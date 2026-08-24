"""Agro-Meteorological Advisory Engine (IMD GKMS / Indic Farmer Intelligence)."""

from typing import Any, Dict, Optional

from weathergpt.core.models import CropAgroAdvisory, GeoLocation, WeatherForecastResponse

# Comprehensive crop advisory database across Indian agro-climatic zones
CROP_ADVISORY_DATABASE: Dict[str, Dict[str, Any]] = {
    "rice": {
        "crop_name": "Paddy (Rice / ধান / धान)",
        "growth_stage": "Tillering & Panicle Initiation (Kharif / Sali)",
        "advisory_en": "Maintain 3-5 cm water level in the field. If heavy rainfall is forecasted, open drainage channels to prevent lodging and bacterial leaf blight.",
        "advisory_hi": "खेत में 3-5 सेमी पानी का स्तर बनाए रखें। भारी बारिश के पूर्वानुमान पर जल निकासी की नालियां खोलें ताकि फसलों को जलभराव और जीवाणु झुलसा रोग से बचाया जा सके।",
        "advisory_as": "পথাৰত ৩-৫ ছে.মি. পানীৰ মাত্ৰা বজাই ৰাখক। প্ৰবল বৰষুণৰ সম্ভাৱনা থাকিলে পানী ওলাই যোৱাৰ সু-ব্যৱস্থা কৰক যাতে ধান গছ ঢলি নপৰে আৰু বেমাৰৰ পৰা ৰক্ষা পৰে।",
        "irrigation_advice": "Do not apply artificial irrigation if precipitation probability exceeds 60%.",
        "fertilizer_pesticide_advice": "Postpone urea top-dressing and fungicide sprays until clear sky conditions prevail.",
        "harvesting_weather_window": "Not applicable for standing vegetative stage.",
    },
    "paddy": {
        "crop_name": "Paddy (Sali Rice / শালি ধান)",
        "growth_stage": "Vegetative / Tillering",
        "advisory_en": "Monitor for stem borer and gall midge. Spray neem-based formulation on clear days only.",
        "advisory_hi": "तना छेदक कीट की निगरानी करें। केवल साफ मौसम में ही नीम आधारित कीटनाशक का छिड़काव करें।",
        "advisory_as": "মাজখোৱা পোকৰ আক্ৰমণ নিৰীক্ষণ কৰক। আকাশ পৰিষ্কাৰ থকা দিনতহে নিমজাতীয় ঔষধ ছটিয়াব।",
        "irrigation_advice": "Ensure adequate soil moisture without prolonged stagnation in nursery beds.",
        "fertilizer_pesticide_advice": "Apply micronutrient zinc sulfate (0.5%) if yellowing appears on lower leaves.",
        "harvesting_weather_window": "Vegetative growth ongoing.",
    },
    "tea": {
        "crop_name": "Tea (চাহ / चाय)",
        "growth_stage": "Flushing & Plucking (Second / Rain Flush)",
        "advisory_en": "With high humidity and intermittent showers, guard against red spider mite and blister blight. Ensure proper clearing of sub-drains in tea estates.",
        "advisory_hi": "उच्च आर्द्रता के कारण लाल मकड़ी कीट और फफोला रोग (ब्लिस्टर ब्लाइट) पर नजर रखें। बागानों में जल निकासी सुचारू रखें।",
        "advisory_as": "উচ্চ আৰ্দ্ৰতাৰ বাবে ৰঙা মকৰা আৰু ব্লিষ্টাৰ ব্লাইটৰ পৰা চাহ গছ সুৰক্ষিত ৰাখক। চাহ বাগিচাত নলা-নৰ্দমা পৰিষ্কাৰ কৰি পানী নিষ্কাশন নিশ্চিত কৰক।",
        "irrigation_advice": "Natural rainfall is sufficient; prevent waterlogging around tea bushes.",
        "fertilizer_pesticide_advice": "Apply copper oxychloride (0.25%) against blister blight after rains subside.",
        "harvesting_weather_window": "Carry out regular 7-8 day plucking rounds on clear mornings.",
    },
    "mustard": {
        "crop_name": "Mustard / Rapeseed (সৰিয়হ / सरसों)",
        "growth_stage": "Land Preparation / Sowing (Rabi)",
        "advisory_en": "Prepare seedbeds with adequate residual soil moisture after monsoon harvest. Treat seeds with Trichoderma viride.",
        "advisory_hi": "मॉनसून फसल की कटाई के बाद पर्याप्त नमी में खेत तैयार करें। बीजों को ट्राइकोडर्मा से उपचारित कर बुवाई करें।",
        "advisory_as": "বাৰিষাৰ শস্য চপোৱাৰ পিছত উপযুক্ত জীপ থকা মাটিত পথাৰ সাজু কৰক। ট্ৰাইক'ডাৰ্মাৰে বীজ শোধন কৰি সিঁচক।",
        "irrigation_advice": "Provide light pre-sowing irrigation if soil moisture is deficient.",
        "fertilizer_pesticide_advice": "Apply baseline dose of Single Super Phosphate (SSP) during final plowing.",
        "harvesting_weather_window": "Sowing phase.",
    },
    "wheat": {
        "crop_name": "Wheat (গেহু / গম)",
        "growth_stage": "Crown Root Initiation / Vegetative",
        "advisory_en": "First irrigation (CRI stage) is critical 20-25 days after sowing. Avoid irrigation if winter rain is predicted.",
        "advisory_hi": "बुवाई के 20-25 दिन बाद सीआरआई (CRI) अवस्था पर पहली सिंचाई अवश्य करें। बारिश की संभावना होने पर सिंचाई टालें।",
        "advisory_as": "সিঁচাৰ ২০-২৫ দিনৰ পাছত প্ৰথম জলসিঞ্চন কৰক। শীতকালীন বৰষুণৰ সম্ভাৱনা থাকিলে জলসিঞ্চন নকৰিব।",
        "irrigation_advice": "Maintain field capacity moisture during crown root development.",
        "fertilizer_pesticide_advice": "Apply first split dose of nitrogen alongside irrigation.",
        "harvesting_weather_window": "Vegetative stage.",
    },
    "jute": {
        "crop_name": "Jute (মৰাপাট / पटसन)",
        "growth_stage": "Harvesting & Retting",
        "advisory_en": "Ideal weather for retting in slow-moving clean water. Harvest mature plants when 50% flowering occurs.",
        "advisory_hi": "पटसन की कटाई और पानी में गलाने (रेडिंग) के लिए मौसम उपयुक्त है। 50% फूल आने पर कटाई करें।",
        "advisory_as": "মৰাপাট কটা আৰু জাগ দিয়াৰ বাবে বতৰ উপযোগী। ৫০% ফুল ফুলাৰ সময়ত মৰাপাট কাটি নিকা পানীত জাগ দিয়ক।",
        "irrigation_advice": "Utilize monsoon ponds and canals for ribbon retting.",
        "fertilizer_pesticide_advice": "No chemical spray needed during retting.",
        "harvesting_weather_window": "Harvest immediately before continuous heavy downpours.",
    },
    "vegetables": {
        "crop_name": "Vegetables & Horticulture (শাক-পাচলি / सब्जियां)",
        "growth_stage": "Fruiting / Maturation",
        "advisory_en": "Provide staking to tomato and chili plants to prevent lodging in gusty winds. Avoid spraying chemicals in windy or rainy hours.",
        "advisory_hi": "तेज हवाओं से बचाव के लिए टमाटर और मिर्च के पौधों को सहारा (स्टेकिंग) दें। बारिश के दौरान रासायनिक छिड़काव न करें।",
        "advisory_as": "বতাহ-বৰষুণৰ পৰা ৰক্ষা কৰিবলৈ বিলাহী আৰু জলকীয়া গছত জেং দি বান্ধক। বৰষুণৰ সময়ত কোনো ঔষধ নিছিটিয়াব।",
        "irrigation_advice": "Provide drip irrigation or furrow irrigation only on non-rainy days.",
        "fertilizer_pesticide_advice": "Spray systemic bio-fungicide only after foliage dries.",
        "harvesting_weather_window": "Harvest ripe fruits before expected afternoon thunderstorms.",
    },
}


class AgroMetService:
    """Delivers GKMS-style agricultural advisories based on meteorological conditions and crop type."""

    def get_advisory_for_crop(
        self,
        crop_query: str,
        loc: GeoLocation,
        forecast: Optional[WeatherForecastResponse] = None,
    ) -> CropAgroAdvisory:
        """Finds matching crop advisory and contextualizes with local weather."""
        q = crop_query.lower().strip()
        matched_key = "rice"
        for key in CROP_ADVISORY_DATABASE:
            if key in q:
                matched_key = key
                break

        data = CROP_ADVISORY_DATABASE[matched_key]

        # Adjust advice if heavy rain is imminent in forecast
        advisory_en = data["advisory_en"]
        advisory_hi = data["advisory_hi"]
        advisory_as = data["advisory_as"]
        irrigation = data["irrigation_advice"]

        if forecast and forecast.current.precipitation_mm > 5.0:
            advisory_en += f" [Alert: Current precipitation in {loc.name} is {forecast.current.precipitation_mm}mm. Ensure field bund drainage.]"
            advisory_hi += f" [सूचना: {loc.name} में वर्तमान में {forecast.current.precipitation_mm} मिमी बारिश है। जल निकास सुनिश्चित करें।]"
            advisory_as += f" [সতৰ্কতা: {loc.name}ত বৰ্তমান {forecast.current.precipitation_mm} মি.মি. বৰষুণ হৈ আছে। পানী নিষ্কাশনৰ ব্যৱস্থা কৰক।]"
            irrigation = "Do NOT irrigate. Natural precipitation is surplus."

        return CropAgroAdvisory(
            crop_name=data["crop_name"],
            growth_stage=data["growth_stage"],
            state=loc.admin1 or "Assam",
            district=loc.admin2 or loc.name,
            advisory_en=advisory_en,
            advisory_hi=advisory_hi,
            advisory_as=advisory_as,
            irrigation_advice=irrigation,
            fertilizer_pesticide_advice=data["fertilizer_pesticide_advice"],
            harvesting_weather_window=data["harvesting_weather_window"],
        )


agromet_service = AgroMetService()
