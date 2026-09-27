"""
Government of India & State-Level Agricultural Schemes & Subsidies Intelligence Harvester.
Deterministic, zero-token access to Central & State farming subsidies, machinery grants,
solar pump incentives, crop insurance, and credit facilities.
"""

from __future__ import annotations
import time
from typing import Dict, Any, List, Optional
from reflex_agent.tools.base import BaseTool, ToolResult

# Comprehensive State-wise and Crop-wise Agricultural Schemes Database
SCHEMES_REGISTRY: List[Dict[str, Any]] = [
    # --- CENTRAL FLAGSHIP SCHEMES (ALL INDIA) ---
    {
        "id": "pm_kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "income_support",
        "level": "Central",
        "states": ["All India"],
        "crops": ["All Crops"],
        "subsidy_amount": "₹6,000 per year (3 equal installments of ₹2,000 via DBT)",
        "objective": "Direct bank transfer income support to all eligible landholding farmer families across India.",
        "eligibility": "All landholding farmer families with cultivable land. Aadhaar-linked bank account and e-KYC mandatory.",
        "documents": ["Aadhaar Card", "Land Khasra / Khatauni Record", "Bank Account Passbook", "Mobile Number"],
        "portal": "https://pmkisan.gov.in",
        "query_hint": "How to check PM-Kisan 19th installment and e-KYC status?"
    },
    {
        "id": "pm_kusum",
        "name": "PM-KUSUM (Solar Agricultural Pump & Grid Scheme)",
        "category": "solar_irrigation",
        "level": "Central",
        "states": ["All India"],
        "crops": ["All Crops"],
        "subsidy_amount": "60% to 90% total financial grant",
        "objective": "Replace diesel pumps with standalone solar irrigation pumps (3 HP to 7.5 HP) and set up solar plants on barren land.",
        "subsidy_breakdown": "Central Govt: 30% | State Govt: 30% (50% in hilly/NE states) | Bank Loan: 30% | Farmer share: 10%–40%",
        "eligibility": "Individual farmers, Farmer Producer Organizations (FPOs), Water User Associations, and Primary Agricultural Credit Societies.",
        "documents": ["Aadhaar Card", "Land Title / Khasra Copy", "Bank Passbook", "Electricity Connection Proof (if grid)"],
        "portal": "https://pmkusum.mnre.gov.in",
        "query_hint": "How much subsidy is available on PM-KUSUM solar pumps and how to apply?"
    },
    {
        "id": "smam_central",
        "name": "SMAM (Sub-Mission on Agricultural Mechanization / Farm Machinery & Drones)",
        "category": "farm_machinery",
        "level": "Central",
        "states": ["All India"],
        "crops": ["All Crops"],
        "subsidy_amount": "40% to 50% individual subsidy (75%-80% for FPOs setting up Custom Hiring Centers)",
        "objective": "Promote farm mechanization with subsidies on tractors, rotavators, super seeders, seed drills, and agricultural drones.",
        "eligibility": "Small and marginal farmers, women farmers, and SC/ST farmers given high priority.",
        "documents": ["Aadhaar Card", "Land Record", "Caste Certificate (if applicable)", "Bank Passbook"],
        "portal": "https://agrimachinery.nic.in",
        "query_hint": "How to get 40% to 50% subsidy on Super Seeder, Rotavator, and Agri Drones under SMAM?"
    },
    {
        "id": "pmfby_insurance",
        "name": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        "category": "crop_insurance",
        "level": "Central",
        "states": ["All India"],
        "crops": ["Paddy", "Wheat", "Soybean", "Cotton", "Mustard", "Maize", "Pulses", "Tomato", "Potato", "Onion"],
        "subsidy_amount": "100% of sum insured payout on verified crop loss",
        "premium_rate": "Kharif Foodgrains & Oilseeds: 2.0% | Rabi crops: 1.5% | Commercial/Horticulture: 5.0% (Govt covers 95-98% premium)",
        "objective": "Comprehensive financial safety net against crop failure due to drought, floods, hailstorms, pest epidemics, and unseasonal rains.",
        "eligibility": "All loanee and non-loanee farmers growing notified crops in notified areas. Mandatory notification within 72 hours of loss via toll-free 14447.",
        "documents": ["Sowing Certificate / Patwari Girdawari", "Aadhaar Card", "Bank Passbook", "Land Khatauni"],
        "portal": "https://pmfby.gov.in",
        "query_hint": "What is the procedure and timeline to file PMFBY insurance claim for crop loss?"
    },
    {
        "id": "kcc_credit",
        "name": "KCC (Kisan Credit Card - Subsidized Crop Loans)",
        "category": "credit_loan",
        "level": "Central",
        "states": ["All India"],
        "crops": ["All Crops"],
        "subsidy_amount": "Only 4% effective annual interest rate (up to ₹3 Lakh)",
        "objective": "Timely institutional credit for crop cultivation, inputs purchase (seeds/fertilizers/pesticides), and post-harvest expenses.",
        "eligibility": "All farmers (owner cultivators, tenant farmers, sharecroppers, and animal husbandry/fishery farmers). Collateral-free up to ₹1.60 Lakh.",
        "documents": ["Application Form", "Identity Proof (Aadhaar/Voter ID)", "Land Ownership Record", "Crop Sowing Self-Declaration"],
        "portal": "https://www.myscheme.gov.in/schemes/kcc",
        "query_hint": "How to get ₹3 Lakh crop loan sanctioned at 4% interest via Kisan Credit Card (KCC)?"
    },
    {
        "id": "soil_health_card",
        "name": "Soil Health Card Scheme",
        "category": "soil_health",
        "level": "Central",
        "states": ["All India"],
        "crops": ["All Crops"],
        "subsidy_amount": "100% Free Laboratory Soil Testing",
        "objective": "Test 12 critical soil nutrient parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) and issue balanced fertilizer prescriptions.",
        "eligibility": "Any Indian farmer can submit soil samples through local Agriculture Extension Officer to receive free health card.",
        "documents": ["Field Khasra Number", "Farmer Aadhaar Number"],
        "portal": "https://soilhealth.dac.gov.in",
        "query_hint": "How to get free soil testing done and generate a Soil Health Card?"
    },
    {
        "id": "pmksy_micro_irrigation",
        "name": "PMKSY (Per Drop More Crop - Drip & Sprinkler Micro-Irrigation)",
        "category": "irrigation",
        "level": "Central",
        "states": ["All India"],
        "crops": ["Sugarcane", "Cotton", "Tomato", "Onion", "Potato", "Paddy", "Maize"],
        "subsidy_amount": "55% (Small/Marginal Farmers) & 45% (Other Farmers) Government Grant",
        "objective": "Save 40-50% water and boost crop yield 30-40% through micro-irrigation systems.",
        "eligibility": "Farmland owners possessing an active irrigation water source (borewell, tubewell, open well, canal).",
        "documents": ["Land Khatauni Copy", "Aadhaar Card", "Bank Passbook", "Irrigation Water Source Certificate"],
        "portal": "https://pmksy.gov.in",
        "query_hint": "How to obtain 55% government subsidy on Drip and Sprinkler Irrigation systems?"
    },

    # --- STATE SPECIFIC SCHEMES ---
    # 1. PUNJAB
    {
        "id": "punjab_crm_stubble",
        "name": "Punjab Crop Residue Management (CRM / In-Situ Stubble Subsidy)",
        "category": "farm_machinery",
        "level": "State",
        "states": ["Punjab"],
        "crops": ["Paddy", "Wheat"],
        "subsidy_amount": "50% for individual farmers | 80% for Cooperatives / FPOs",
        "objective": "Heavy subsidies on Super Seeder, Happy Seeder, Smart Seeder, Straw Chopper, and Baler for in-situ stubble management without burning.",
        "eligibility": "Punjab farmers with valid registration on the Punjab Agriculture Portal.",
        "documents": ["Aadhaar Card", "Punjab Land Revenue Fard", "Bank Passbook", "Tractor RC"],
        "portal": "https://agrimachinery.nic.in",
        "query_hint": "How to apply for 50% to 80% stubble management subsidy on Super Seeder in Punjab?"
    },
    {
        "id": "punjab_paani_bachao",
        "name": "Pani Bachao Paise Kamao (Save Water Earn Money Scheme)",
        "category": "irrigation",
        "level": "State",
        "states": ["Punjab"],
        "crops": ["Paddy", "Wheat"],
        "subsidy_amount": "₹4 per kWh direct bank transfer (DBT) on electricity saved",
        "objective": "Conserve underground water aquifers by providing cash incentives for reducing tubewell power usage.",
        "eligibility": "Agricultural electricity consumers registered with PSPCL in Punjab.",
        "documents": ["Tubewell Electricity Bill / Account Number", "Aadhaar Card", "Bank Account Details"],
        "portal": "https://pspcl.in",
        "query_hint": "How to claim ₹4/unit incentive under Punjab Pani Bachao Paise Kamao scheme?"
    },

    # 2. HARYANA
    {
        "id": "haryana_mera_pani",
        "name": "Mera Pani Meri Virasat (Crop Diversification Incentive)",
        "category": "crop_diversification",
        "level": "State",
        "states": ["Haryana"],
        "crops": ["Paddy", "Maize", "Cotton", "Pulses"],
        "subsidy_amount": "₹7,000 per acre financial incentive",
        "objective": "Financial assistance for shifting from water-intensive paddy to maize, cotton, pulses, or keeping land fallow.",
        "eligibility": "Haryana farmers who register alternative crops on the Meri Fasal Mera Byora portal.",
        "documents": ["Meri Fasal Mera Byora Registration", "Aadhaar Card", "Bank Passbook"],
        "portal": "https://fasal.haryana.gov.in",
        "query_hint": "How to get ₹7,000/acre incentive for switching from paddy to maize or cotton in Haryana?"
    },
    {
        "id": "haryana_bhavantar_horticulture",
        "name": "Bhavantar Bharpayee Yojana (Horticulture Price Deficit Payment)",
        "category": "market_price_support",
        "level": "State",
        "states": ["Haryana"],
        "crops": ["Tomato", "Onion", "Potato", "Cauliflower", "Carrot", "Peas"],
        "subsidy_amount": "100% price deficit coverage between Mandi price and Protected Base Rate",
        "objective": "Protect vegetable growers when market prices crash (Protected Base Rate: Tomato ₹400/Qtl, Onion ₹650/Qtl, Potato ₹600/Qtl).",
        "eligibility": "Haryana horticulture farmers registered on Meri Fasal Mera Byora portal.",
        "documents": ["Crop Registration Slip", "APMC Mandi J-Form", "Bank Account Passbook"],
        "portal": "https://agriharyana.gov.in",
        "query_hint": "How to receive price deficiency compensation under Bhavantar Bharpayee for tomato and onion?"
    },

    # 3. UTTAR PRADESH
    {
        "id": "up_kisan_uday",
        "name": "Uttar Pradesh Kisan Uday Yojana (Energy Efficient Solar Pumps)",
        "category": "solar_irrigation",
        "level": "State",
        "states": ["Uttar Pradesh"],
        "crops": ["All Crops"],
        "subsidy_amount": "100% Free distribution of 5HP to 7.5HP energy-efficient solar/smart electric pump sets",
        "objective": "Replace inefficient obsolete pumps with modern solar and smart energy-saving pumps with zero power bills.",
        "eligibility": "Small and marginal farmers of Uttar Pradesh possessing cultivable land and water source.",
        "documents": ["Certified Land Khatauni Copy", "Aadhaar Card", "Domicile Certificate", "Bank Passbook"],
        "portal": "http://upagriculture.com",
        "query_hint": "What is the eligibility to get a free solar pump set under UP Kisan Uday Yojana?"
    },
    {
        "id": "up_yantra_subsidy",
        "name": "UP Farm Machinery Subsidy Token System",
        "category": "farm_machinery",
        "level": "State",
        "states": ["Uttar Pradesh"],
        "crops": ["Wheat", "Paddy", "Sugarcane", "Mustard", "Potato"],
        "subsidy_amount": "40% to 50% direct DBT grant (up to ₹1 Lakh)",
        "objective": "Subsidies on rotavators, laser land levelers, cultivators, multicrop threshers, and power sprayers via online token lottery.",
        "eligibility": "All UP farmers registered on the Pardarshi Kisan Seva portal (upagriculture.com).",
        "documents": ["Farmer Registration Number", "Aadhaar Card", "Bank Passbook"],
        "portal": "http://upagriculture.com",
        "query_hint": "How to book an online token for rotavator and thresher subsidy in Uttar Pradesh?"
    },
    {
        "id": "up_e_ganna",
        "name": "UP e-Ganna & Sugarcane Supply Calendar (Cane SAP & Parchi)",
        "category": "market_price_support",
        "level": "State",
        "states": ["Uttar Pradesh"],
        "crops": ["Sugarcane"],
        "subsidy_amount": "State Advised Price (SAP ₹370/Qtl) and direct supply slip quota",
        "objective": "Eliminate middlemen commission through transparent weighment, instant SMS parchis, and direct mill-to-bank payments.",
        "eligibility": "Registered sugarcane farmers in Uttar Pradesh.",
        "documents": ["Sugarcane Satta Code", "Aadhaar Card", "Bank Passbook"],
        "portal": "https://caneup.in",
        "query_hint": "How to check sugarcane supply calendar and ₹370/quintal payment on UP e-Ganna portal?"
    },

    # 4. MADHYA PRADESH
    {
        "id": "mp_kisan_kalyan",
        "name": "MP Mukhyamantri Kisan Kalyan Yojana",
        "category": "income_support",
        "level": "State",
        "states": ["Madhya Pradesh"],
        "crops": ["All Crops"],
        "subsidy_amount": "₹4,000 per year State top-up (Total ₹10,000/year combined with PM-KISAN)",
        "objective": "Provide an additional ₹4,000 (in 2 equal installments) from MP State Govt to all PM-Kisan eligible farmers.",
        "eligibility": "Domicile farmers of Madhya Pradesh verified under the PM-KISAN scheme.",
        "documents": ["Samagra ID", "Aadhaar Card", "PM-KISAN Registration ID", "Bank Account Passbook"],
        "portal": "https://saara.mp.gov.in",
        "query_hint": "How to check MP Mukhyamantri Kisan Kalyan Yojana ₹4,000 installment using Samagra ID?"
    },
    {
        "id": "mp_bhavantar_bhugtan",
        "name": "MP Bhavantar Bhugtan Yojana (Price Deficiency Payment)",
        "category": "market_price_support",
        "level": "State",
        "states": ["Madhya Pradesh"],
        "crops": ["Soybean", "Maize", "Urad", "Moong", "Groundnut"],
        "subsidy_amount": "Direct bank transfer of price gap between MSP and Mandi Modal Rate",
        "objective": "Protect soybean, maize, and pulse growers from distress sales below MSP through deficit compensation.",
        "eligibility": "Madhya Pradesh farmers registered and verified on the e-Uparjan portal.",
        "documents": ["e-Uparjan Registration Slip", "APMC Mandi Weighment Slip / Anugya Patra", "Aadhaar Card"],
        "portal": "http://mpeuparjan.nic.in",
        "query_hint": "How to claim Bhavantar deficiency compensation if Indore Mandi soybean rates fall below MSP?"
    },

    # 5. MAHARASHTRA
    {
        "id": "maha_namo_shetkari",
        "name": "Namo Shetkari Mahasanman Nidhi Yojana",
        "category": "income_support",
        "level": "State",
        "states": ["Maharashtra"],
        "crops": ["All Crops"],
        "subsidy_amount": "₹6,000 per year State grant (Total ₹12,000/year combined with PM-KISAN)",
        "objective": "Provide an additional ₹6,000 annually to Maharashtra farmers to assist with input cultivation costs.",
        "eligibility": "All PM-KISAN verified farmer families in Maharashtra.",
        "documents": ["Aadhaar Card", "7/12 Extract and 8-A Extract", "Bank Passbook"],
        "portal": "https://mahadbt.maharashtra.gov.in",
        "query_hint": "How to check Maharashtra Namo Shetkari ₹6,000 installment and 7/12 linking status?"
    },
    {
        "id": "maha_magel_tyala_shet_tale",
        "name": "Magel Tyala Shettale (Farm Pond on Demand Maharashtra)",
        "category": "irrigation",
        "level": "State",
        "states": ["Maharashtra"],
        "crops": ["Cotton", "Soybean", "Sugarcane", "Paddy", "Onion"],
        "subsidy_amount": "Direct government grant up to ₹75,000 (including plastic lining)",
        "objective": "Construct on-farm rainwater harvesting ponds to provide protective life-saving irrigation for cotton, soybean, and onion.",
        "eligibility": "Maharashtra farmers holding at least 0.60 hectares of land.",
        "documents": ["7/12 Extract", "Aadhaar Card", "Bank Passbook", "Consent Letter"],
        "portal": "https://mahadbt.maharashtra.gov.in",
        "query_hint": "How to receive ₹75,000 grant under Magel Tyala Shettale scheme for digging a farm pond?"
    },

    # 6. RAJASTHAN
    {
        "id": "raj_tarbandi",
        "name": "Rajasthan Tarbandi Wire Fencing Subsidy Scheme",
        "category": "farm_protection",
        "level": "State",
        "states": ["Rajasthan"],
        "crops": ["Wheat", "Mustard", "Bajra", "Gram", "Cotton"],
        "subsidy_amount": "50% of fencing cost (up to ₹40,000 to ₹48,000)",
        "objective": "Protect standing crops from nilgai and stray animals by installing barbed wire perimeter fencing around farm fields.",
        "eligibility": "Farmers holding minimum 1.5 hectares of cultivable land (individual or group).",
        "documents": ["Jamabandi Land Record Copy (under 6 months old)", "Aadhaar Card", "Jan Aadhaar Card", "Bank Passbook"],
        "portal": "https://rajkisan.rajasthan.gov.in",
        "query_hint": "How to get 50% government subsidy (₹48,000) for farm boundary wire fencing in Rajasthan?"
    },
    {
        "id": "raj_drip_micro",
        "name": "Rajasthan Drip & Sprinkler Micro-Irrigation Subsidy",
        "category": "irrigation",
        "level": "State",
        "states": ["Rajasthan"],
        "crops": ["Mustard", "Wheat", "Bajra", "Tomato", "Pomegranate"],
        "subsidy_amount": "70% to 75% Government Subsidy (for small, marginal, and women farmers)",
        "objective": "Ensure bumper harvest of mustard and pomegranate in arid regions with micro-drip and sprinkler systems.",
        "eligibility": "All Rajasthan farmers possessing an irrigation well/tubewell or water storage diggi.",
        "documents": ["Jamabandi Copy", "Jan Aadhaar Card", "Bank Diary Passbook", "Electricity Bill / Pump Receipt"],
        "portal": "https://rajkisan.rajasthan.gov.in",
        "query_hint": "How to apply for 75% subsidy on sprinkler and drip irrigation systems in Rajasthan?"
    },

    # 7. KARNATAKA
    {
        "id": "karnataka_raitha_siri",
        "name": "Karnataka Raitha Siri Millet Incentive Scheme",
        "category": "crop_diversification",
        "level": "State",
        "states": ["Karnataka"],
        "crops": ["Millets (Ragi, Jowar, Bajra)", "Paddy", "Maize"],
        "subsidy_amount": "₹10,000 per hectare direct financial incentive (up to 2 hectares)",
        "objective": "Promote cultivation of nutritious minor millets (Ragi, Jowar, Foxtail, Little millet) and preserve groundwater.",
        "eligibility": "Karnataka farmers who register their land on the FRUITS portal.",
        "documents": ["FRUITS FID Number", "Aadhaar Card", "Bank Passbook", "Pahani (RTC) Record"],
        "portal": "https://fruits.karnataka.gov.in",
        "query_hint": "How to claim ₹10,000/hectare incentive for cultivating millets (Ragi/Jowar) under Raitha Siri?"
    },

    # 8. TRIPURA & NORTH EAST REGION
    {
        "id": "tripura_movcd_ner",
        "name": "MOVCD-NER (Mission Organic Value Chain Development for North East)",
        "category": "organic_farming",
        "level": "State",
        "states": ["Tripura"],
        "crops": ["Tomato", "Paddy", "Ginger", "Turmeric", "Pineapple", "Mustard"],
        "subsidy_amount": "₹50,000 per hectare assistance (over 3 years) + 100% Free Organic Certification",
        "objective": "Promote zero chemical and chemical-free organic farming with direct market linkages to organic export clusters.",
        "eligibility": "Farmers in Tripura and Northeast who join certified Organic Farmer Producer Companies (FPCs).",
        "documents": ["Aadhaar Card", "Land Record Parcha (ROR)", "Bank Passbook", "FPO Membership Slip"],
        "portal": "https://agri.tripura.gov.in",
        "query_hint": "How to get ₹50,000/hectare subsidy and free organic certification under MOVCD-NER in Tripura?"
    },
    {
        "id": "tripura_solar_hilly",
        "name": "Tripura Solar Water Pump Special Hilly Subsidy Grant",
        "category": "solar_irrigation",
        "level": "State",
        "states": ["Tripura"],
        "crops": ["Paddy", "Tomato", "Potato", "Vegetables"],
        "subsidy_amount": "85% to 90% total government grant (farmer share only 10%)",
        "objective": "Deploy solar energy and gravity-fed irrigation in Tilla (hilly) and Lunga (valley) terrain across Tripura.",
        "eligibility": "Small, marginal, and Scheduled Tribe (ST) farmers of Tripura.",
        "documents": ["Citizen Identity Card", "Land Khatian Record", "Bank Account Details"],
        "portal": "https://treda.tripura.gov.in",
        "query_hint": "How to install a solar water pump with 90% subsidy in the Tilla regions of Tripura?"
    }
]


class GovtSchemesTool(BaseTool):
    """
    State-wise and Crop-wise Government of India and State Agricultural Intelligence Harvester.
    Provides sub-5ms deterministic lookup without incurring LLM token costs.
    """
    name: str = "gov_schemes"
    description: str = "Query Central and State agricultural schemes, subsidies, machinery grants, solar pump incentives, crop insurance, and Kisan Credit Card facilities filtered by State and Crop."
    category: str = "agriculture"
    is_destructive: bool = False

    def execute(self, query: str = "pm_kisan", state: Optional[str] = None, crop: Optional[str] = None, category: Optional[str] = None, **kwargs) -> ToolResult:
        start = time.perf_counter()
        results = self.filter_schemes(state=state, crop=crop, category=category, search_text=query)
        elapsed = (time.perf_counter() - start) * 1000.0

        # Backward compatibility with test assertions
        primary = results[0] if results else SCHEMES_REGISTRY[0]
        scheme_info = dict(primary)
        scheme_info["official_name"] = primary.get("name", "")
        scheme_info["subsidy_details"] = primary.get("subsidy_amount", "")

        return ToolResult(
            success=True,
            output={
                "matched_scheme": primary.get("id", "pm_kisan"),
                "scheme_info": scheme_info,
                "total_matched": len(results),
                "schemes": results,
                "available_states": self.get_available_states(),
                "available_crops": self.get_available_crops(),
                "query_context": {
                    "query": query,
                    "state": state or "All India",
                    "crop": crop or "All Crops",
                    "category": category or "All Categories"
                }
            },
            execution_time_ms=round(elapsed, 2)
        )

    @classmethod
    def filter_schemes(
        cls,
        state: Optional[str] = None,
        crop: Optional[str] = None,
        category: Optional[str] = None,
        search_text: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Pure deterministic filter over schemes registry.
        Executes in < 1ms with 0 LLM tokens.
        """
        matched = []
        st_norm = state.strip().lower() if state and state.strip().lower() not in ["all", "all india", "all states", "सभी राज्य"] else None
        cr_norm = crop.strip().lower() if crop and crop.strip().lower() not in ["all", "all crops", "सभी फसलें"] else None
        cat_norm = category.strip().lower() if category and category.strip().lower() not in ["all", "all categories", "सभी श्रेणियां"] else None
        q_norm = search_text.strip().lower() if search_text else None

        for s in SCHEMES_REGISTRY:
            # 1. State check
            if st_norm:
                states_lower = [st.lower() for st in s["states"]]
                if "all india" not in states_lower and st_norm not in states_lower:
                    continue

            # 2. Crop check
            if cr_norm:
                crops_lower = [c.lower() for c in s["crops"]]
                if "all crops" not in crops_lower and not any(cr_norm in c or c in cr_norm for c in crops_lower):
                    continue

            # 3. Category check
            if cat_norm:
                if cat_norm != s["category"].lower() and cat_norm not in s["category"].lower():
                    continue

            # 4. Search text keyword match (if provided)
            if q_norm and len(q_norm) > 2 and q_norm not in ["pm_kisan", "all"]:
                searchable_blob = f"{s['name']} {s['objective']} {s['id']} {s.get('subsidy_amount', '')} {' '.join(s['states'])} {' '.join(s['crops'])}".lower()
                # Split tokens
                tokens = [t for t in q_norm.replace("-", " ").replace("_", " ").split() if len(t) > 2]
                if tokens and not any(t in searchable_blob for t in tokens):
                    continue

            matched.append(s)

        # If nothing matched search query, fallback to state/crop matches
        if not matched and (st_norm or cr_norm):
            return [s for s in SCHEMES_REGISTRY if "all india" in [st.lower() for st in s["states"]]][:4]

        return matched if matched else SCHEMES_REGISTRY[:6]

    @classmethod
    def get_available_states(cls) -> List[str]:
        states_set = set()
        for s in SCHEMES_REGISTRY:
            for st in s["states"]:
                states_set.add(st)
        sorted_states = sorted([s for s in states_set if s != "All India"])
        return ["All India"] + sorted_states

    @classmethod
    def get_available_crops(cls) -> List[str]:
        crops_set = set()
        for s in SCHEMES_REGISTRY:
            for cr in s["crops"]:
                crops_set.add(cr)
        sorted_crops = sorted([c for c in crops_set if c != "All Crops"])
        return ["All Crops"] + sorted_crops

    @classmethod
    def get_available_categories(cls) -> List[str]:
        return [
            "income_support",
            "solar_irrigation",
            "farm_machinery",
            "crop_insurance",
            "credit_loan",
            "irrigation",
            "soil_health",
            "crop_diversification",
            "market_price_support",
            "organic_farming",
            "farm_protection"
        ]

    def get_routing_criteria(self) -> str:
        return "Used when farmer queries government schemes, state subsidies, solar pump grants, machinery subsidies, crop insurance, PM-KISAN, or state welfare schemes for specific states and crops."
