"""
Geo-Intelligence & Agro-Climatic Observational Tool for KisanZess.
Brought directly from l-data-seT---ML to provide satellite spectral telemetry (NDVI, NDWI, EVI),
sowing calendars, KVK advisories, and historical climate analytics for major agricultural zones.
"""

from typing import Dict, Any, Optional
from reflex_agent.tools.base import BaseTool, ToolResult

LOCATION_PROFILES = {
    "indore": {
        "name": "Indore & Malwa Plateau",
        "state": "Madhya Pradesh",
        "lat": 22.7196,
        "lng": 75.8577,
        "agro_zone": "Central Plateau & Hills (ICAR Zone VIII)",
        "soil_type": "Deep Black Cotton Soil (Vertisols)",
        "avg_annual_rainfall_mm": 950,
        "monsoon_profile": "SW Monsoon concentrated (Jun-Sep ~90%)",
        "climate_classification": "Tropical Wet and Dry / Semi-Arid",
        "current_weather": {
            "temperature": 26.0,
            "humidity": 65,
            "ph": 7.1,
            "rainfall": 180,
            "N": 90,
            "P": 45,
            "K": 40
        },
        "ndvi_vegetation_index": 0.65,
        "vegetation_status": "Active Soybean & Cotton Canopy",
        "historical_climate_summary": "Deep cracking montmorillonite clay allows high moisture retention. Ideal for soybean kharif followed by wheat/gram rabi rotation.",
        "top_historical_crops": ["Soybean", "Cotton", "Wheat", "Gram / Chickpea"],
        "drought_risk": "Moderate",
        "flood_risk": "Low (Good natural drainage)",
        "spectral_indices": {
            "ndvi": 0.65,
            "ndvi_status": "Healthy Vegetative Cover",
            "ndwi": 0.38,
            "ndwi_status": "Optimal Canopy Hydration",
            "evi": 0.52,
            "evi_status": "Moderate-to-High Biomass Index",
            "soil_moisture_pct": 26.0,
            "soil_moisture_status": "26% Moisture in Vertisol Topsoil",
            "canopy_temp_c": 25.4
        },
        "sowing_calendar": {
            "stage": "Soybean Pod Filling & Cotton First Picking",
            "optimal_window": "Jun 20 – Jul 10 (Kharif) / Oct 15 – Nov 15 (Rabi)",
            "days_to_monsoon": 0,
            "monsoon_name": "SW Monsoon Withdrawal Stage",
            "soil_workability": "Excellent for zero-till rabi sowing"
        },
        "mandi_prices": [
            { "crop": "Soybean (Yellow)", "mandi": "Indore Main Mandi", "price": 4650, "msp": 4600, "change": "+2.6%", "trend": "Bullish" },
            { "crop": "Cotton (Medium Staple)", "mandi": "Khargone APMC", "price": 7250, "msp": 6620, "change": "+1.8%", "trend": "Steady" },
            { "crop": "Wheat (Lokwan / Sharbati)", "mandi": "Dewas Mandi", "price": 2650, "msp": 2275, "change": "+3.1%", "trend": "High Demand" }
        ],
        "kvk_advisory": "Soybean pod borer (Helicoverpa) surveillance active. If 2 larvae/meter row observed, apply Neem Seed Kernel Extract (NSKE 5%) or Chlorantraniliprole 18.5 SC @ 60ml/acre. Avoid indiscriminate synthetic pyrethroid sprays."
    },
    "thanjavur": {
        "name": "Thanjavur (Cauvery Delta Rice Bowl)",
        "state": "Tamil Nadu",
        "lat": 10.7870,
        "lng": 79.1378,
        "agro_zone": "Cauvery Deltaic Zone",
        "soil_type": "Deep Heavy Clay Alluvium (Regur/Clayey)",
        "avg_annual_rainfall_mm": 1050,
        "monsoon_profile": "NE Monsoon peak (Oct-Dec), Canal irrigation fed by Cauvery Mettur dam",
        "climate_classification": "Tropical Semi-Arid to Sub-Humid",
        "current_weather": {
            "temperature": 28.0,
            "humidity": 80,
            "ph": 6.7,
            "rainfall": 210,
            "N": 92,
            "P": 45,
            "K": 40
        },
        "ndvi_vegetation_index": 0.74,
        "vegetation_status": "Intense Paddy Field Canopy",
        "historical_climate_summary": "Century-long multi-cropping history with Kuruvai, Samba, and Thaladi rice seasons followed by blackgram pulse fallow.",
        "top_historical_crops": ["Rice / Paddy", "Blackgram", "Banana", "Sugarcane"],
        "drought_risk": "Moderate (Dependent on river inflows)",
        "flood_risk": "Moderate in low-lying delta canals",
        "spectral_indices": {
            "ndvi": 0.74,
            "ndvi_status": "Peak Vegetative Canopy",
            "ndwi": 0.52,
            "ndwi_status": "High Surface Water Content (Puddled Soil)",
            "evi": 0.62,
            "evi_status": "Very High Biomass Index",
            "soil_moisture_pct": 34.0,
            "soil_moisture_status": "34.0% Saturated Clay Moisture",
            "canopy_temp_c": 26.5
        },
        "sowing_calendar": {
            "stage": "Samba Paddy Main Field Transplanting",
            "optimal_window": "Sep 25 – Oct 30",
            "days_to_monsoon": 18,
            "monsoon_name": "Cauvery Peak Discharge Window",
            "soil_workability": "Ideal for mechanical rice transplanter"
        },
        "mandi_prices": [
            { "crop": "Paddy (CR-1009 / ADT-45)", "mandi": "Thanjavur Regulated", "price": 2420, "msp": 2300, "change": "+2.1%", "trend": "Bullish" },
            { "crop": "Blackgram (Vamban-8)", "mandi": "Kumbakonam", "price": 8100, "msp": 7400, "change": "+4.2%", "trend": "High Demand" }
        ],
        "kvk_advisory": "Humid delta weather favors blast and bacterial leaf blight. Apply 25kg Zinc Sulphate per hectare as basal dressing. Refrain from top-dressing urea during continuous overcast cloudy spells."
    },
    "ludhiana": {
        "name": "Ludhiana (Central Plain Punjab)",
        "state": "Punjab",
        "lat": 30.9010,
        "lng": 75.8573,
        "agro_zone": "Trans-Gangetic Plains Zone",
        "soil_type": "Indo-Gangetic Deep Loam & Silt",
        "avg_annual_rainfall_mm": 680,
        "monsoon_profile": "SW Monsoon (Jul-Aug) + Western Disturbances (Dec-Feb)",
        "climate_classification": "Subtropical Semi-Arid",
        "current_weather": {
            "temperature": 22.0,
            "humidity": 60,
            "ph": 7.4,
            "rainfall": 110,
            "N": 105,
            "P": 48,
            "K": 35
        },
        "ndvi_vegetation_index": 0.78,
        "vegetation_status": "High Biomass Crop Stand",
        "historical_climate_summary": "Extensive tubewell & canal network support high-yield input-intensive Paddy-Wheat system.",
        "top_historical_crops": ["Basmati Rice", "Wheat", "Maize", "Mustard"],
        "drought_risk": "Low (Irrigation secured)",
        "flood_risk": "Low",
        "spectral_indices": {
            "ndvi": 0.78,
            "ndvi_status": "Very High Biomass Stand",
            "ndwi": 0.48,
            "ndwi_status": "Hydrated Rootzone",
            "evi": 0.66,
            "evi_status": "Optimal Photosynthetic Stand",
            "soil_moisture_pct": 29.0,
            "soil_moisture_status": "29% Moisture",
            "canopy_temp_c": 21.0
        },
        "sowing_calendar": {
            "stage": "Paddy Maturation & Pre-Wheat Field Preparation",
            "optimal_window": "Nov 1 – Nov 20 (Wheat)",
            "days_to_monsoon": 0,
            "monsoon_name": "Winter Sowing Transition",
            "soil_workability": "Super-seeder in-situ residue management"
        },
        "mandi_prices": [
            { "crop": "Basmati 1121", "mandi": "Khanna APMC", "price": 3950, "msp": 2300, "change": "+5.1%", "trend": "Strong Export Demand" },
            { "crop": "Wheat (HD-2967)", "mandi": "Ludhiana Mandi", "price": 2525, "msp": 2275, "change": "+1.9%", "trend": "Stable" }
        ],
        "kvk_advisory": "Adopt in-situ stubble management with Super Seeder / Happy Seeder. Incorporating straw adds 15kg N, 5kg P, and 60kg K back into the soil, saving ₹1,200/acre in fertilizer cost."
    },
    "nashik": {
        "name": "Nashik & Lasalgaon (Maharashtra)",
        "state": "Maharashtra",
        "lat": 19.9975,
        "lng": 73.7898,
        "agro_zone": "Western Maharashtra Scarcity Zone",
        "soil_type": "Black Basaltic Regur & Clay Loam",
        "avg_annual_rainfall_mm": 800,
        "monsoon_profile": "Ghat rain shadow, heavy early monsoon (Jun-Aug)",
        "climate_classification": "Tropical Wet and Dry",
        "current_weather": {
            "temperature": 24.5,
            "humidity": 68,
            "ph": 6.9,
            "rainfall": 140,
            "N": 70,
            "P": 44,
            "K": 60
        },
        "ndvi_vegetation_index": 0.61,
        "vegetation_status": "Horticultural & Onion Canopy",
        "historical_climate_summary": "Asia's largest onion market hub. High thermal range favorable for table grapes, pomegranates, and rabi onions.",
        "top_historical_crops": ["Onion", "Table Grapes", "Pomegranate", "Tomato"],
        "drought_risk": "Moderate",
        "flood_risk": "Low",
        "spectral_indices": {
            "ndvi": 0.61,
            "ndvi_status": "Active Canopy",
            "ndwi": 0.35,
            "ndwi_status": "Moderate Hydration",
            "evi": 0.49,
            "evi_status": "Healthy Foliage",
            "soil_moisture_pct": 24.0,
            "soil_moisture_status": "24% Moisture",
            "canopy_temp_c": 24.0
        },
        "sowing_calendar": {
            "stage": "Late Kharif Onion Nursery & Grape Pruning",
            "optimal_window": "Oct 1 – Nov 15",
            "days_to_monsoon": 0,
            "monsoon_name": "Post-Monsoon Horticultural Phase",
            "soil_workability": "Drip irrigation bed preparation"
        },
        "mandi_prices": [
            { "crop": "Onion (Red)", "mandi": "Lasalgaon APMC", "price": 3100, "msp": 1800, "change": "+12.0%", "trend": "Bullish" },
            { "crop": "Table Grapes", "mandi": "Pimpalgaon", "price": 8500, "msp": 6000, "change": "+4.0%", "trend": "High Value" }
        ],
        "kvk_advisory": "Onion thrips and purple blotch monitoring: spray Mancozeb 75 WP @ 2.5g/L water mixed with spreader. Keep nursery beds well-drained."
    }
}


class GeoIntelligenceTool(BaseTool):
    """
    Provides regional agro-climatic, spectral NDVI, and KVK advisory intelligence.
    """
    name: str = "geo_intelligence"
    description: str = "Query regional agro-climatic telemetry, satellite NDVI/NDWI indices, sowing windows, and KVK advisories by hub or district."
    category: str = "agriculture"
    is_destructive: bool = False

    def execute(self, region: str = "indore", **kwargs) -> ToolResult:
        key = region.lower().strip()
        found_key = None
        for k in LOCATION_PROFILES.keys():
            if k in key or key in k:
                found_key = k
                break
        
        if not found_key:
            found_key = "indore"

        profile = LOCATION_PROFILES[found_key]
        return ToolResult(
            success=True,
            output={
                "region_key": found_key,
                "name": profile["name"],
                "state": profile["state"],
                "agro_zone": profile["agro_zone"],
                "soil_type": profile["soil_type"],
                "weather": profile["current_weather"],
                "ndvi_score": profile["ndvi_vegetation_index"],
                "vegetation_status": profile["vegetation_status"],
                "spectral": profile["spectral_indices"],
                "sowing_calendar": profile["sowing_calendar"],
                "mandi_prices": profile["mandi_prices"],
                "kvk_advisory": profile["kvk_advisory"]
            }
        )

    def get_routing_criteria(self) -> str:
        return "Used when farmer asks about regional weather, agro-climatic zones, satellite NDVI telemetry, sowing calendar, or KVK advisories."
