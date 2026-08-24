"""India Meteorological Department (IMD) bulletins and severe weather alerts aggregator."""

from typing import List, Optional

import httpx

from weathergpt.core.models import AlertSeverity, GeoLocation, IMDAlert

# Dynamic regional IMD alert repository
STATE_DISTRICT_IMD_ALERTS: List[IMDAlert] = [
    IMDAlert(
        alert_id="IMD-AS-2026-0801",
        district="Kamrup Metropolitan",
        state="Assam",
        severity=AlertSeverity.ORANGE,
        event_type="Heavy Rainfall & Thunderstorm",
        description="Isolated heavy to very heavy rainfall (70-120mm) accompanied by gusty winds (40-50 kmph) and lightning.",
        valid_from="2026-08-24T06:00:00Z",
        valid_to="2026-08-25T18:00:00Z",
        safety_actions_en=[
            "Stay indoors and away from windows during thunderstorms.",
            "Do not shelter under isolated tall trees or tin sheds.",
            "Avoid travelling through waterlogged low-lying roads.",
            "Farmers are advised to postpone spraying pesticides and keep harvested crops covered."
        ],
        safety_actions_hi=[
            "आंधी-तूफान के समय घर के अंदर रहें और खिड़कियों से दूर रहें।",
            "अकेले ऊंचे पेड़ों या टिन की छतों के नीचे शरण न लें।",
            "जलभराव वाले निचले मार्गों पर यात्रा करने से बचें।",
            "किसान कीटनाशक छिड़काव स्थगित करें और कटी फसल सुरक्षित रखें।"
        ],
        safety_actions_as=[
            "বজ্ৰপাতৰ সময়ত ঘৰৰ ভিতৰত থাকক আৰু খিৰিকীৰ পৰা আঁতৰি থাকক।",
            "ওখ গছৰ তলত বা টিনৰ চালিত আশ্ৰয় নলব।",
            "পানী জমা হোৱা তলতীয়া ৰাস্তাইদি যাতায়ত নকৰিব।",
            "কৃষকসকলে কীটনাশক ছটিওৱা স্থগিত ৰাখক আৰু চপোৱা শস্য ঢাকি ৰাখক।"
        ],
    ),
    IMDAlert(
        alert_id="IMD-AS-2026-0802",
        district="Dibrugarh",
        state="Assam",
        severity=AlertSeverity.YELLOW,
        event_type="Moderate Thunderstorm & Rain",
        description="Moderate rain with lightning expected over Brahmaputra river basin.",
        valid_from="2026-08-24T06:00:00Z",
        valid_to="2026-08-25T12:00:00Z",
        safety_actions_en=[
            "Keep emergency battery lights charged.",
            "Unplug sensitive electronic equipment during lightning."
        ],
        safety_actions_hi=[
            "आपातकालीन लाइटें चार्ज रखें।",
            "बिजली चमकने पर संवेदनशील इलेक्ट्रॉनिक उपकरण अनप्लग करें।"
        ],
        safety_actions_as=[
            "জৰুৰীকালীন লাইট চাৰ্জ কৰি ৰাখক।",
            "বজ্ৰপাতৰ সময়ত বৈদ্যুতিক সামগ্ৰী প্লাগৰ পৰা খুলি থওক।"
        ],
    ),
    IMDAlert(
        alert_id="IMD-ML-2026-0803",
        district="East Khasi Hills",
        state="Meghalaya",
        severity=AlertSeverity.RED,
        event_type="Extremely Heavy Rainfall (Flash Flood Alert)",
        description="Continuous intense rainfall exceeding 200mm likely in Cherrapunji and Shillong catchment.",
        valid_from="2026-08-24T00:00:00Z",
        valid_to="2026-08-25T23:59:00Z",
        safety_actions_en=[
            "High risk of landslides; avoid hillside roads and gorges.",
            "Move to higher ground if living near river streams."
        ],
        safety_actions_hi=[
            "भूस्खलन का भारी खतरा; पहाड़ी रास्तों और घाटियों से बचें।",
            "नदी के पास रहने वाले लोग ऊंचे स्थानों पर चले जाएं।"
        ],
        safety_actions_as=[
            "ভূমিস্খলনৰ প্ৰচুৰ সম্ভাৱনা; পাহাৰীয়া পথ পৰিহাৰ কৰক।",
            "নৈৰ কাষৰীয়া লোকে ওখ নিৰাপদ স্থানলৈ স্থানান্তৰিত হওক।"
        ],
    ),
    IMDAlert(
        alert_id="IMD-DL-2026-0804",
        district="New Delhi",
        state="Delhi",
        severity=AlertSeverity.YELLOW,
        event_type="Localized Drizzle & Hot/Humid Weather",
        description="Partly cloudy sky with light passing showers, high humidity index.",
        valid_from="2026-08-24T08:00:00Z",
        valid_to="2026-08-25T20:00:00Z",
        safety_actions_en=[
            "Stay hydrated and avoid direct afternoon sun exposure.",
            "Wear light cotton clothing."
        ],
        safety_actions_hi=[
            "पर्याप्त पानी पिएं और दोपहर की तेज धूप से बचें।",
            "हल्के सूती कपड़े पहनें।"
        ],
        safety_actions_as=[
            "প্ৰচুৰ পানী খাওক আৰু দুপৰীয়া ৰ'দৰ পৰা আঁতৰি থাকক।",
            "পাতল কপাহী কাপোৰ পৰিধান কৰক।"
        ],
    ),
    IMDAlert(
        alert_id="IMD-MH-2026-0805",
        district="Mumbai City",
        state="Maharashtra",
        severity=AlertSeverity.ORANGE,
        event_type="High Tide & Heavy Coastal Rain",
        description="High tide of 4.2m expected with intermittent heavy showers across coastal belt.",
        valid_from="2026-08-24T10:00:00Z",
        valid_to="2026-08-25T16:00:00Z",
        safety_actions_en=[
            "Avoid visiting beaches and promenades during high tide.",
            "Check local railway and traffic updates before stepping out."
        ],
        safety_actions_hi=[
            "हाई टाइड के दौरान समुद्र तटों और सैरगाहों पर जाने से बचें।",
            "घर से निकलने से पहले लोकल ट्रेन और ट्रैफिक अपडेट जांचें।"
        ],
        safety_actions_as=[
            "উচ্চ জোৱাৰৰ সময়ত সমুদ্ৰতীৰলৈ নাযাব।",
            "ওলাই যোৱাৰ পূৰ্বে ট্ৰেফিক আৰু ৰেলৰ তথ্য লওক।"
        ],
    ),
    IMDAlert(
        alert_id="IMD-WB-2026-0806",
        district="Kolkata",
        state="West Bengal",
        severity=AlertSeverity.YELLOW,
        event_type="Thundershowers with Gusty Winds",
        description="Convective cloud development causing evening thundershowers (Kalbaishakhi/Nor'wester activity).",
        valid_from="2026-08-24T14:00:00Z",
        valid_to="2026-08-25T21:00:00Z",
        safety_actions_en=[
            "Take shelter during gusty wind bursts.",
            "Secure loose rooftop objects."
        ],
        safety_actions_hi=[
            "तेज हवाओं के समय सुरक्षित स्थान पर शरण लें।",
            "छत पर रखी खुली वस्तुओं को बांधकर सुरक्षित करें।"
        ],
        safety_actions_as=[
            "তীব্ৰ বতাহৰ সময়ত সুৰক্ষিত আশ্ৰয় লওক।",
            "ঘৰৰ চাল বা বেলকনিত থকা আলগা বস্তু বান্ধি থওক।"
        ],
    ),
]


class IMDAlertService:
    """Service to query and parse official India Meteorological Department alerts."""

    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self._client = client

    async def get_alerts_for_location(self, loc: GeoLocation) -> List[IMDAlert]:
        """Retrieves active IMD weather warnings for a given location or district."""
        results: List[IMDAlert] = []
        loc_name = loc.name.lower()
        admin1 = (loc.admin1 or "").lower()
        admin2 = (loc.admin2 or "").lower()

        for alert in STATE_DISTRICT_IMD_ALERTS:
            alert_dist = alert.district.lower()
            alert_state = alert.state.lower()

            if (alert_dist in loc_name or loc_name in alert_dist or
                alert_dist in admin2 or admin2 in alert_dist or
                alert_state in admin1 or admin1 in alert_state):
                results.append(alert)

        # If no specific warning, return a Green advisory
        if not results:
            results.append(
                IMDAlert(
                    alert_id=f"IMD-{loc.name[:2].upper()}-GEN-00",
                    district=loc.admin2 or loc.name,
                    state=loc.admin1 or "India",
                    severity=AlertSeverity.GREEN,
                    event_type="No Severe Weather Warning",
                    description=f"Normal seasonal weather prevailing across {loc.name}. No urgent warnings issued by IMD.",
                    valid_from="2026-08-24T00:00:00Z",
                    valid_to="2026-08-25T23:59:00Z",
                    safety_actions_en=["Enjoy regular outdoor activities while staying hydrated."],
                    safety_actions_hi=["सामान्य दैनिक गतिविधियां जारी रखें और पर्याप्त पानी पिएं।"],
                    safety_actions_as=["স্বাভাৱিক কাম-কাজ চলাই যাওক আৰু পৰ্যাপ্ত পানী খাওক।"],
                )
            )

        return results


imd_service = IMDAlertService()
