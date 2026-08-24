"""Geocoding service with high-resolution Indian locations and Open-Meteo API fallback."""

from typing import Dict, Optional

import httpx

from weathergpt.core.config import settings
from weathergpt.core.logger import logger
from weathergpt.core.models import GeoLocation

# High-precision registry of major Indian cities, agricultural hubs, and North-East districts
INDIC_LOCATIONS_DATABASE: Dict[str, GeoLocation] = {
    # Assam & North East
    "guwahati": GeoLocation(
        name="Guwahati", latitude=26.1445, longitude=91.7362, admin1="Assam", admin2="Kamrup Metropolitan", population=957345
    ),
    "dibrugarh": GeoLocation(
        name="Dibrugarh", latitude=27.4728, longitude=94.9120, admin1="Assam", admin2="Dibrugarh", population=154019
    ),
    "silchar": GeoLocation(
        name="Silchar", latitude=24.8333, longitude=92.7789, admin1="Assam", admin2="Cachar", population=172830
    ),
    "jorhat": GeoLocation(
        name="Jorhat", latitude=26.7509, longitude=94.2037, admin1="Assam", admin2="Jorhat", population=153889
    ),
    "tezpur": GeoLocation(
        name="Tezpur", latitude=26.6338, longitude=92.7926, admin1="Assam", admin2="Sonitpur", population=102505
    ),
    "nagaon": GeoLocation(
        name="Nagaon", latitude=26.3468, longitude=92.6840, admin1="Assam", admin2="Nagaon", population=147137
    ),
    "shillong": GeoLocation(
        name="Shillong", latitude=25.5788, longitude=91.8933, admin1="Meghalaya", admin2="East Khasi Hills", population=143229
    ),
    "cherrapunji": GeoLocation(
        name="Cherrapunji (Sohra)", latitude=25.2702, longitude=91.7323, admin1="Meghalaya", admin2="East Khasi Hills", population=14816
    ),
    "agartala": GeoLocation(
        name="Agartala", latitude=23.8315, longitude=91.2868, admin1="Tripura", admin2="West Tripura", population=400004
    ),
    "imphal": GeoLocation(
        name="Imphal", latitude=24.8170, longitude=93.9368, admin1="Manipur", admin2="Imphal West", population=268243
    ),
    "kohima": GeoLocation(
        name="Kohima", latitude=25.6751, longitude=94.1086, admin1="Nagaland", admin2="Kohima", population=99039
    ),
    "aizawl": GeoLocation(
        name="Aizawl", latitude=23.7271, longitude=92.7176, admin1="Mizoram", admin2="Aizawl", population=293416
    ),
    "itanagar": GeoLocation(
        name="Itanagar", latitude=27.0844, longitude=93.6053, admin1="Arunachal Pradesh", admin2="Papum Pare", population=59490
    ),
    "gangtok": GeoLocation(
        name="Gangtok", latitude=27.3389, longitude=88.6065, admin1="Sikkim", admin2="East Sikkim", population=100286
    ),
    # Major Metros & States
    "delhi": GeoLocation(
        name="New Delhi", latitude=28.6139, longitude=77.2090, admin1="Delhi", admin2="New Delhi", population=33000000
    ),
    "mumbai": GeoLocation(
        name="Mumbai", latitude=19.0760, longitude=72.8777, admin1="Maharashtra", admin2="Mumbai City", population=21000000
    ),
    "bengaluru": GeoLocation(
        name="Bengaluru", latitude=12.9716, longitude=77.5946, admin1="Karnataka", admin2="Bangalore Urban", population=13000000
    ),
    "bangalore": GeoLocation(
        name="Bengaluru", latitude=12.9716, longitude=77.5946, admin1="Karnataka", admin2="Bangalore Urban", population=13000000
    ),
    "kolkata": GeoLocation(
        name="Kolkata", latitude=22.5726, longitude=88.3639, admin1="West Bengal", admin2="Kolkata", population=15000000
    ),
    "chennai": GeoLocation(
        name="Chennai", latitude=13.0827, longitude=80.2707, admin1="Tamil Nadu", admin2="Chennai", population=11000000
    ),
    "hyderabad": GeoLocation(
        name="Hyderabad", latitude=17.3850, longitude=78.4867, admin1="Telangana", admin2="Hyderabad", population=10000000
    ),
    "pune": GeoLocation(
        name="Pune", latitude=18.5204, longitude=73.8567, admin1="Maharashtra", admin2="Pune", population=7000000
    ),
    "jaipur": GeoLocation(
        name="Jaipur", latitude=26.9124, longitude=75.7873, admin1="Rajasthan", admin2="Jaipur", population=4000000
    ),
    "lucknow": GeoLocation(
        name="Lucknow", latitude=26.8467, longitude=80.9462, admin1="Uttar Pradesh", admin2="Lucknow", population=3800000
    ),
    "patna": GeoLocation(
        name="Patna", latitude=25.5941, longitude=85.1376, admin1="Bihar", admin2="Patna", population=2500000
    ),
    "ahmedabad": GeoLocation(
        name="Ahmedabad", latitude=23.0225, longitude=72.5714, admin1="Gujarat", admin2="Ahmedabad", population=8000000
    ),
    "bhopal": GeoLocation(
        name="Bhopal", latitude=23.2599, longitude=77.4126, admin1="Madhya Pradesh", admin2="Bhopal", population=2400000
    ),
    "chandigarh": GeoLocation(
        name="Chandigarh", latitude=30.7333, longitude=76.7794, admin1="Chandigarh", admin2="Chandigarh", population=1200000
    ),
    "shimla": GeoLocation(
        name="Shimla", latitude=31.1048, longitude=77.1734, admin1="Himachal Pradesh", admin2="Shimla", population=170000
    ),
    "srinagar": GeoLocation(
        name="Srinagar", latitude=34.0837, longitude=74.7973, admin1="Jammu and Kashmir", admin2="Srinagar", population=1500000
    ),
    "bhubaneswar": GeoLocation(
        name="Bhubaneswar", latitude=20.2961, longitude=85.8245, admin1="Odisha", admin2="Khordha", population=1100000
    ),
    "thiruvananthapuram": GeoLocation(
        name="Thiruvananthapuram", latitude=8.5241, longitude=76.9366, admin1="Kerala", admin2="Thiruvananthapuram", population=1000000
    ),
    "coimbatore": GeoLocation(
        name="Coimbatore", latitude=11.0168, longitude=76.9558, admin1="Tamil Nadu", admin2="Coimbatore", population=2000000
    ),
    "varanasi": GeoLocation(
        name="Varanasi", latitude=25.3176, longitude=82.9739, admin1="Uttar Pradesh", admin2="Varanasi", population=1400000
    ),
}

# In-memory geocoding cache
_GEOCODING_CACHE: Dict[str, GeoLocation] = {}


class GeocodingService:
    """Provides high-accuracy location resolution across India with online and offline fallbacks."""

    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self._client = client

    def _normalize_name(self, name: str) -> str:
        cleaned = name.strip().lower()
        cleaned = cleaned.replace("city", "").replace("district", "").replace("in ", "").replace("at ", "").strip()
        # Handle Indic scripts transliteration hints if needed
        hindi_map = {
            "दिल्ली": "delhi", "नई दिल्ली": "delhi", "गुवाहाटी": "guwahati", "डिब्रूगढ़": "dibrugarh",
            "सिलचर": "silchar", "मुंबई": "mumbai", "कोलकाता": "kolkata", "चेन्नई": "chennai",
            "बेंगलुरु": "bengaluru", "जयपुर": "jaipur", "लखनऊ": "lucknow", "पटना": "patna",
            "শিলচৰ": "silchar", "গুৱাহাটী": "guwahati", "ডিব্ৰুগড়": "dibrugarh", "যোৰহাট": "jorhat",
            "তেজপুৰ": "tezpur", "নগাঁও": "nagaon"
        }
        for k, v in hindi_map.items():
            if k in cleaned:
                return v
        return cleaned

    async def resolve_location(self, query: str) -> GeoLocation:
        """Resolves city/region query into GeoLocation with lat/lon."""
        normalized = self._normalize_name(query)

        # 1. Check in-memory cache
        if normalized in _GEOCODING_CACHE:
            return _GEOCODING_CACHE[normalized]

        # 2. Check local Indic database (instant exact or prefix match)
        if normalized in INDIC_LOCATIONS_DATABASE:
            loc = INDIC_LOCATIONS_DATABASE[normalized]
            _GEOCODING_CACHE[normalized] = loc
            return loc

        for key, loc in INDIC_LOCATIONS_DATABASE.items():
            if key in normalized or normalized in key:
                _GEOCODING_CACHE[normalized] = loc
                return loc

        # 3. Query Open-Meteo Geocoding API if online
        try:
            url = f"{settings.openmeteo_geocoding_url}/search"
            params = {"name": query, "count": 1, "language": "en", "format": "json"}

            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    if results:
                        item = results[0]
                        resolved = GeoLocation(
                            name=item.get("name", query.title()),
                            latitude=float(item.get("latitude")),
                            longitude=float(item.get("longitude")),
                            country=item.get("country", "India"),
                            admin1=item.get("admin1"),
                            admin2=item.get("admin2"),
                            timezone=item.get("timezone", "Asia/Kolkata"),
                            elevation=item.get("elevation"),
                            population=item.get("population"),
                        )
                        _GEOCODING_CACHE[normalized] = resolved
                        return resolved
        except Exception as e:
            logger.warning(f"Remote geocoding error for '{query}': {e}. Falling back to default location.")

        # 4. Fallback default (Guwahati/New Delhi if unknown)
        fallback = GeoLocation(
            name=query.title() if query else "Guwahati",
            latitude=26.1445,
            longitude=91.7362,
            country="India",
            admin1="Assam",
            admin2="Kamrup Metropolitan",
        )
        _GEOCODING_CACHE[normalized] = fallback
        return fallback


geocoding_service = GeocodingService()
