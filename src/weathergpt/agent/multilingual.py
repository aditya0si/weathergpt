"""Indic Multilingual processor for English, Hindi, and Assamese."""

import re
from typing import Dict

from weathergpt.core.models import LanguageCode

ASSAMESE_CHARACTERS = set("ৰৱ")  # Distinct Assamese graphemes: Ra (U+09F0), Va (U+09F1)
ASSAMESE_COMMON_WORDS = {
    "বতৰ", "বৰষুণ", "আজি", "কাইলৈ", "অসম", "গুৱাহাটী", "ধান", "চাহ", "বজ্ৰপাত",
    "ধুমুহা", "উষ্ণতা", "কৃষি", "পথাৰ", "বায়ু", "বানপানী", "শস্য", "সৰিয়হ",
    "কেতিয়া", "কেনেকুৱা", "হবনে", "পৰামৰ্শ", "বৰদৈচিলা", "কিনকিনীয়া"
}

HINDI_COMMON_WORDS = {
    "मौसम", "बारिश", "आज", "कल", "तापमान", "हवा", "आंधी", "तूफान", "कृषि",
    "फसल", "किसान", "चेतावनी", "गर्मी", "सर्दी", "चावल", "धान", "गेहूं", "सरसों",
    "कैसा", "रहेगा", "क्या", "होगी", "बताओ", "सलाह", "प्रदूषण", "हवा"
}


def detect_language(text: str) -> LanguageCode:
    """Detects whether text is Assamese, Hindi, or English."""
    cleaned = text.strip()
    if not cleaned:
        return LanguageCode.EN

    # Check for distinct Assamese letters (ৰ, ৱ)
    if any(c in ASSAMESE_CHARACTERS for c in cleaned):
        return LanguageCode.AS

    # Check for Assamese specific vocabulary
    words = set(re.findall(r"[\u0980-\u09FF]+", cleaned))
    if words and len(words.intersection(ASSAMESE_COMMON_WORDS)) > 0:
        return LanguageCode.AS

    # Check for Bengali/Assamese Unicode script block (\u0980-\u09FF)
    bengali_assamese_chars = len(re.findall(r"[\u0980-\u09FF]", cleaned))
    if bengali_assamese_chars >= 2:
        return LanguageCode.AS

    # Check for Devanagari Unicode script block (\u0900-\u097F)
    devanagari_chars = len(re.findall(r"[\u0900-\u097F]", cleaned))
    if devanagari_chars >= 2:
        return LanguageCode.HI

    # Check for Hindi words in Latin script (Hinglish check)
    lower_words = set(cleaned.lower().split())
    if any(w in lower_words for w in ["kaisa", "hogi", "barish", "mausam", "aaj", "kal", "kisan"]):
        return LanguageCode.HI

    return LanguageCode.EN


# Indic Lexicon and Response Templates
INDIC_GLOSSARY: Dict[str, Dict[LanguageCode, str]] = {
    "current_weather_heading": {
        LanguageCode.EN: "Current Weather in",
        LanguageCode.HI: "में वर्तमान मौसम",
        LanguageCode.AS: "ৰ বৰ্তমান বতৰ",
    },
    "temperature": {
        LanguageCode.EN: "Temperature",
        LanguageCode.HI: "तापमान",
        LanguageCode.AS: "উষ্ণতা",
    },
    "feels_like": {
        LanguageCode.EN: "Feels like",
        LanguageCode.HI: "महसूस होता है",
        LanguageCode.AS: "অনুভৱ হোৱা উষ্ণতা",
    },
    "humidity": {
        LanguageCode.EN: "Humidity",
        LanguageCode.HI: "आर्द्रता / नमी",
        LanguageCode.AS: "আৰ্দ্ৰতা",
    },
    "wind": {
        LanguageCode.EN: "Wind Speed",
        LanguageCode.HI: "हवा की गति",
        LanguageCode.AS: "বতাহৰ গতি",
    },
    "precipitation": {
        LanguageCode.EN: "Precipitation / Rain",
        LanguageCode.HI: "बारिश",
        LanguageCode.AS: "বৰষুণ",
    },
    "air_quality": {
        LanguageCode.EN: "Air Quality Index (AQI)",
        LanguageCode.HI: "वायु गुणवत्ता सूचकांक (AQI)",
        LanguageCode.AS: "বায়ুৰ গুণমান সূচক (AQI)",
    },
    "alerts_warning": {
        LanguageCode.EN: "IMD Weather Warning",
        LanguageCode.HI: "मौसम विभाग की चेतावनी",
        LanguageCode.AS: "বতৰ বিজ্ঞান কেন্দ্ৰৰ সতৰ্কবাৰ্তা",
    },
    "agromet_heading": {
        LanguageCode.EN: "Agricultural Advisory (GKMS)",
        LanguageCode.HI: "कृषि मौसम परामर्श (ग्रामीण कृषि मौसम सेवा)",
        LanguageCode.AS: "কৃষি বতৰ পৰামৰ্শ (গ্ৰামীণ কৃষি বতৰ সেৱা)",
    },
    "climate_heading": {
        LanguageCode.EN: "Climate Science & Meteorology Explanation",
        LanguageCode.HI: "जलवायु विज्ञान एवं मौसम संबंधी जानकारी",
        LanguageCode.AS: "জলবায়ু বিজ্ঞান আৰু বতৰ বিজ্ঞান সম্পৰ্কীয় তথ্য",
    },
}
