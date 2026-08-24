"""Climate science knowledge base and FAQ repository for Indian meteorological phenomena."""

from typing import List, Optional

from weathergpt.core.models import ClimateKnowledgeFact

CLIMATE_FACTS_REGISTRY: List[ClimateKnowledgeFact] = [
    ClimateKnowledgeFact(
        topic="monsoon_sw",
        keywords=["southwest monsoon", "sw monsoon", "summer monsoon", "monsoon onset", "barish", "বাৰিষা", "বাৰিষাকাল", "मॉनसून"],
        title="Southwest Monsoon (দক্ষিণ-পশ্চিম মৌচুমী / दक्षिण-पश्चिम मॉनसून)",
        explanation_en=(
            "The Southwest Monsoon is India's primary rainfall mechanism (June-September), contributing ~75% of total annual precipitation. "
            "It is driven by intense thermal heating over the Tibetan Plateau creating low pressure, which pulls moisture-laden oceanic winds "
            "from the southern Indian Ocean across the equator and into the Arabian Sea and Bay of Bengal branches."
        ),
        explanation_hi=(
            "दक्षिण-पश्चिम मॉनसून (जून से सितंबर) भारत का प्रमुख वर्षा तंत्र है, जो वार्षिक वर्षा का लगभग 75% प्रदान करता है। "
            "यह तिब्बती पठार पर अत्यधिक गर्मी के कारण बने निम्न दबाव क्षेत्र से प्रेरित होता है, जो हिंद महासागर से नमी युक्त मानसूनी हवाओं को अपनी ओर खींचता है।"
        ),
        explanation_as=(
            "দক্ষিণ-পশ্চিম মৌচুমী বায়ু (জুনৰ পৰা ছেপ্টেম্বৰ) ভাৰতৰ মুখ্য বৰ্ষাকালীন ব্যৱস্থা, যি মুঠ বাৰ্ষিক বৰষুণৰ প্ৰায় ৭৫% যোগান ধৰে। "
            "তিব্বত মালভূমিত হোৱা তীব্ৰ উত্তাপৰ ফলত সৃষ্টি হোৱা নিম্নচাপে ভাৰত মহাসাগৰৰ পৰা জলীয় বাষ্পযুক্ত বায়ুক বংগোপসাগৰ আৰু আৰৱ সাগৰ হৈ দেশখনলৈ আকৰ্ষণ কৰে।"
        ),
        scientific_basis="Differential heating between landmass and Indian Ocean; Inter-Tropical Convergence Zone (ITCZ) northward migration.",
        source_agency="India Meteorological Department (IMD) / MoES",
    ),
    ClimateKnowledgeFact(
        topic="bordoisila",
        keywords=["bordoisila", "kalbaishakhi", "norwester", "বৰদৈচিলা", "কালবৈশাখী", "thunder squall", "pre monsoon"],
        title="Bordoisila & Kalbaishakhi Pre-Monsoon Squalls (বৰদৈচিলা / कालবৈশাখী)",
        explanation_en=(
            "Bordoisila (in Assam) and Kalbaishakhi (in Bengal) are intense pre-monsoon localized convective storms occurring between March and May. "
            "In Assamese folklore, Bordoisila represents a young married woman flying hastily back to her mother's home with furious wind and rain. "
            "Scientifically, they are severe thunderstorms triggered by warm moist air from the Bay of Bengal colliding with cooler dry westerlies over the Chota Nagpur plateau and Brahmaputra valley."
        ),
        explanation_hi=(
            "बोरदोईसिला (असम) और कालवैशाखी (बंगाल) मार्च से मई के दौरान आने वाले तीव्र प्री-मॉनसून आंधी-तूफान हैं। "
            "असमिया लोककथाओं में बोरदोईसिला एक विवाहिता का प्रतीक है जो तेज हवा और बारिश के साथ अपने मायके लौटती है। वैज्ञानिक रूप से यह बंगाल की खाड़ी की नम हवा और उत्तर-पश्चिमी शुष्क हवाओं के टकराव से उत्पन्न होते हैं।"
        ),
        explanation_as=(
            "বৰদৈচিলা হৈছে চ'ত-ব'হাগ মাহত অসম আৰু উত্তৰ-পূৰ্বাঞ্চলত হোৱা তীব্ৰ প্ৰাক-মৌচুমী ধুমুহা-বৰষুণ। "
            "অসমীয়া লোকবিশ্বাস অনুসৰি বৰদৈচিলা হৈছে মাকৰ ঘৰলৈ উভতি অহা বাউলী জীয়াৰীৰ প্ৰতীক। বৈজ্ঞানিকভাৱে, বংগোপসাগৰৰ পৰা অহা আৰ্দ্ৰ বায়ু আৰু শুকান শীতল পশ্চিমীয়া বায়ুৰ সংঘৰ্ষৰ ফলত এই প্ৰচণ্ড বিজুলী-ঢেৰেকনিযুক্ত ধুমুহাৰ সৃষ্টি হয়।"
        ),
        scientific_basis="Severe mesoscale convective systems (MCS) with CAPE > 2500 J/kg and strong vertical wind shear.",
        source_agency="Regional Meteorological Centre Guwahati / IMD",
    ),
    ClimateKnowledgeFact(
        topic="western_disturbance",
        keywords=["western disturbance", "wd", "winter rain", "snowfall", "पश्चिमी विक्षोभ", "শীতকালীন বৰষুণ"],
        title="Western Disturbances (पश्चिमी विक्षोभ / পশ্চিমীয়া ঝঞ্ঝা)",
        explanation_en=(
            "A Western Disturbance is an extratropical cyclone originating over the Mediterranean Sea, Caspian Sea, and Atlantic Ocean. "
            "It travels eastward embedded in the subtropical westerly jet stream, bringing essential winter rain to North-Western India (crucial for the Rabi wheat crop) and heavy snowfall to the Himalayas."
        ),
        explanation_hi=(
            "पश्चिमी विक्षोभ एक अतिरिक्त-उष्णकटिबंधीय चक्रवात है जो भूमध्य सागर और कैस्पियन सागर से उत्पन्न होता है। "
            "यह जेट स्ट्रीम के सहारे पूर्व की ओर बढ़ता है और उत्तर-पश्चिम भारत में महत्वपूर्ण शीतकालीन वर्षा (रबी गेहूं के लिए आवश्यक) तथा हिमालय में भारी बर्फबारी लाता है।"
        ),
        explanation_as=(
            "পশ্চিমীয়া ঝঞ্ঝা হৈছে ভূমধ্য সাগৰ আৰু কাস্পিয়ান সাগৰৰ পৰা উৎপত্তি হোৱা এক বহিঃক্ৰান্তীয় ঘূৰ্ণীবতাহ। "
            "ই চাব-ট্ৰপিকেল জে'ট ষ্ট্ৰিমৰ জৰিয়তে পূব দিশলৈ গতি কৰি উত্তৰ-পশ্চিম ভাৰতত শীতকালীন বৰষুণ (ৰবি শস্যৰ বাবে অতি লাগতিয়াল) আৰু হিমালয়ত বৰফপাত ঘটায়।"
        ),
        scientific_basis="Mid-tropospheric cyclonic vorticity advection in the Subtropical Westerly Jet (SWJ).",
        source_agency="National Centre for Medium Range Weather Forecasting (NCMRWF) / IMD",
    ),
    ClimateKnowledgeFact(
        topic="el_nino_iod",
        keywords=["el nino", "la nina", "enso", "iod", "indian ocean dipole", "এল নিনো", "एल नीनो", "লা নিনা"],
        title="ENSO & Indian Ocean Dipole (এল নিনো আৰু ভাৰত মহাসাগৰীয় ডাইপোল)",
        explanation_en=(
            "El Niño refers to anomalous warming of the central/eastern equatorial Pacific sea surface temperatures, historically associated with weakened Indian summer monsoons. "
            "Conversely, a Positive Indian Ocean Dipole (IOD) features warmer western Indian Ocean waters, which often counteracts El Niño and enhances rainfall across the subcontinent."
        ),
        explanation_hi=(
            "एल नीनो भूमध्यरेखीय प्रशांत महासागर के गर्म होने की घटना है, जो अक्सर भारतीय मॉनसून को कमजोर करती है। "
            "इसके विपरीत, पॉजिटिव इंडियन ओशन डिपोल (IOD) पश्चिमी हिंद महासागर को गर्म करता है, जो एल नीनो के प्रभाव को कम करके भारत में अच्छी बारिश कराने में मदद करता है।"
        ),
        explanation_as=(
            "এল নিনো হৈছে প্ৰশান্ত মহাসাগৰৰ বিষুৱীয় অঞ্চলৰ সাগৰীয় পৃষ্ঠৰ অস্বাভাৱিক উত্তাপ, যাৰ ফলত প্ৰায়ে ভাৰতীয় মৌচুমী বৰষুণ দুৰ্বল হয়। "
            "আনহাতে, পজিটিভ ইণ্ডিয়ান অ'চেন ডাইপোল (IOD)ত পশ্চিম ভাৰত মহাসাগৰৰ পানী অধিক গৰম হয়, যিয়ে এল নিনোৰ ঋণাত্মক প্ৰভাৱ প্ৰতিৰোধ কৰি বৰষুণ বৃদ্ধিত সহায় কৰে।"
        ),
        scientific_basis="Coupled ocean-atmosphere teleconnections; Walker circulation shift.",
        source_agency="Ministry of Earth Sciences (MoES) / IMD",
    ),
    ClimateKnowledgeFact(
        topic="cyclones_india",
        keywords=["cyclone", "tropical cyclone", "bay of bengal", "arabian sea", "ঘূৰ্ণীবতাহ", "चक्रवात", "toofan"],
        title="Tropical Cyclogenesis in Bay of Bengal & Arabian Sea (ক্ৰান্তীয় ঘূৰ্ণীবতাহ)",
        explanation_en=(
            "India experiences two distinct tropical cyclone seasons: Pre-monsoon (April-May) and Post-monsoon (October-December). "
            "The Bay of Bengal witnesses roughly 4 times more cyclones than the Arabian Sea due to high sea surface temperatures (>28°C), low vertical wind shear, and influx of remnant typhoons from the South China Sea."
        ),
        explanation_hi=(
            "भारत में उष्णकटिबंधीय चक्रवातों के दो मुख्य मौसम होते हैं: प्री-मॉनसून (अप्रैल-मई) और पोस्ट-मॉनसून (अक्टूबर-दिसंबर)। "
            "बंगाल की खाड़ी में उच्च समुद्री तापमान (>28°C) और अनुकूल वायुमंडलीय स्थितियों के कारण अरब सागर की तुलना में 4 गुना अधिक चक्रवात आते हैं।"
        ),
        explanation_as=(
            "ভাৰতত ক্ৰান্তীয় ঘূৰ্ণীবতাহৰ দুটা মুখ্য সময় থাকে: প্ৰাক-মৌচুমী (এপ্ৰিল-মে') আৰু উত্তৰ-মৌচুমী (অক্টোবৰ-ডিচেম্বৰ)। "
            "বংগোপসাগৰৰ সাগৰীয় পৃষ্ঠৰ উচ্চ উত্তাপ (>২৮° চেলছিয়াছ) আৰু অনুকুল বতাহৰ বাবে আৰৱ সাগৰৰ তুলনাত ইয়াত প্ৰায় ৪ গুণ অধিক ঘূৰ্ণীবতাহৰ উৎপত্তি হয়।"
        ),
        scientific_basis="Coriolis force, Low-level relative vorticity, Sea Surface Temperature (SST) >= 26.5°C.",
        source_agency="Cyclone Warning Division, IMD New Delhi",
    ),
    ClimateKnowledgeFact(
        topic="heatwaves_urban_heat_island",
        keywords=["heatwave", "heat wave", "loo", "लू", "গৰমৰ প্ৰকোপ", "উত্তাপ তৰংগ", "urban heat island"],
        title="Heatwaves & Urban Heat Islands in India (लू আৰু নগৰীয়া উত্তাপ দ্বীপ)",
        explanation_en=(
            "IMD declares a Heatwave when the maximum temperature reaches at least 40°C in plains (30°C in hills) with departure from normal >= 4.5°C. "
            "Hot, dry winds blowing from Thar desert across North-Central India are known as 'Loo'. Dense urban concrete and lack of green cover exacerbate this through the Urban Heat Island (UHI) effect."
        ),
        explanation_hi=(
            "मैदानी इलाकों में जब तापमान कम से कम 40°C (पहाड़ों में 30°C) तक पहुंच जाए और सामान्य से 4.5°C अधिक हो, तो मौसम विभाग 'लू' या हीटवेव घोषित करता है। "
            "कंक्रीट की इमारतों और हरियाली की कमी के कारण शहरों में 'अर्बन हीट आइलैंड' का प्रभाव बढ़ जाता है।"
        ),
        explanation_as=(
            "সমতল ভূমিত সৰ্বোচ্চ উষ্ণতা ৪০° চেলছিয়াছ (পাহাৰত ৩০° চেলছিয়াছ) আৰু স্বাভাৱিকতকৈ ৪.৫° অধিক হ'লে বতৰ বিজ্ঞানে উত্তাপ তৰংগ (Heatwave) ঘোষণা কৰে। "
            "নগৰাঞ্চলৰ পকী নিৰ্মাণ আৰু গছ-গছনিৰ অভাৱৰ ফলত 'আৰ্বান হিট আইলেণ্ড'ৰ সৃষ্টি হৈ নিশাৰ ভাগতো উষ্ণতা স্বাভাৱিকতকৈ বেছি থাকে।"
        ),
        scientific_basis="Thermal advection, anti-cyclonic subsidence over NW India, nocturnal radiant trapping in urban canopies.",
        source_agency="IMD National Weather Forecasting Centre",
    ),
]


class ClimateKnowledgeService:
    """Delivers verified climate science facts, meteorological definitions, and synoptic explanations."""

    def search_climate_knowledge(self, query: str) -> Optional[ClimateKnowledgeFact]:
        """Performs semantic/keyword lookup over the Indian climate knowledge base."""
        q = query.lower().strip()

        # 1. Exact keyword match
        for fact in CLIMATE_FACTS_REGISTRY:
            for kw in fact.keywords:
                if kw in q:
                    return fact

        # 2. Topic/Token match
        for fact in CLIMATE_FACTS_REGISTRY:
            if fact.topic in q or any(tok in q for tok in fact.topic.split("_")):
                return fact

        # Default fallback to Southwest Monsoon if broadly asking about climate
        if any(w in q for w in ["climate", "weather system", "meteorology", "atmosphere", "হাওয়া"]):
            return CLIMATE_FACTS_REGISTRY[0]

        return None


climate_kb_service = ClimateKnowledgeService()
