"""Tests for KisanZess Agricultural Modules.

Covers:
1. MandiPriceTool (deterministic APMC rates)
2. SoilCropRecommendationTool (Scikit-Learn ML)
3. FertilizerScheduleTool (NPK Deficit)
4. FarmMemoryVault (Persistent farmer context)
5. KrishiPanchayatWarRoom (4-Agent consensus)
"""

import pytest
from reflex_agent.tools.builtin.mandi_tool import MandiPriceTool
from reflex_agent.tools.builtin.agri_ml import SoilCropRecommendationTool, FertilizerScheduleTool
from reflex_agent.memory.farm_vault import FarmMemoryVault, FarmerProfile
from reflex_agent.reasoning.krishi_panchayat import KrishiPanchayatWarRoom


def test_mandi_price_tool():
    tool = MandiPriceTool()
    res = tool.execute(crop="tomato", district="Agartala")
    assert res.success is True
    assert "modal_price" in res.output
    assert "₹" in res.output["modal_price"]
    assert res.output["crop"].lower() == "tomato"


def test_soil_crop_recommendation_tool():
    tool = SoilCropRecommendationTool()
    res = tool.execute(N=90, P=42, K=43, ph=6.5, rainfall=180.0)
    assert res.success is True
    assert "top_recommendations" in res.output
    assert len(res.output["top_recommendations"]) > 0


def test_fertilizer_schedule_tool():
    tool = FertilizerScheduleTool()
    res = tool.execute(crop="paddy", nitrogen=40, phosphorus=20, potassium=30)
    assert res.success is True
    assert "recommended_fertilizer" in res.output
    assert "deficits" in res.output


def test_farm_memory_vault(tmp_path):
    vault_file = tmp_path / "test_vault.json"
    vault = FarmMemoryVault(storage_path=str(vault_file))
    
    profile = FarmerProfile(
        farmer_id="test_farmer_99",
        name="Sunita Devi",
        district="Agartala",
        state="Tripura",
        land_acres=2.5,
        soil_type="Alluvial"
    )
    vault.register_or_update(profile)
    retrieved = vault.get_profile("test_farmer_99")
    assert retrieved is not None
    assert retrieved.name == "Sunita Devi"
    
    ctx = vault.get_context_for_prompt("test_farmer_99")
    assert "Sunita Devi" in ctx
    assert "Alluvial" in ctx


def test_krishi_panchayat():
    warroom = KrishiPanchayatWarRoom()
    consensus = warroom.deliberate(
        query="टमाटर पर सफेद मक्खी का हमला",
        crop="Tomato",
        mandi_rate_per_quintal=3500.0,
        acreage=2.0
    )
    assert len(consensus.opinions) == 3
    assert consensus.sarpanch_synthesis_hindi != ""
    assert consensus.sarpanch_synthesis_english != ""
    assert consensus.total_estimated_budget_inr > 0
    assert consensus.economic_viability_score >= 0.8


def test_hermes_memory_and_skill_loop(tmp_path):
    vault_file = tmp_path / "hermes_vault.json"
    vault = FarmMemoryVault(storage_path=str(vault_file))
    
    # 1. Test Skill Refinement
    skill = vault.learn_skill_from_outcome(
        district="Indore",
        crop="Soybean",
        skill_name="Indore Sticky Trap Protocol",
        proven_rule="Deploy 20 yellow sticky traps per acre to halt early whitefly infestation."
    )
    assert skill["skill_name"] == "Indore Sticky Trap Protocol"
    
    skills = vault.get_learned_skills(district="Indore", crop="Soybean")
    assert len(skills) == 1
    assert "yellow sticky traps" in skills[0]["rule"]
    
    # 2. Test FARM_MEMORY.md export
    mem_file = tmp_path / "FARM_MEMORY.md"
    content = vault.export_hermes_memory_md(farmer_id="farmer_001", output_path=str(mem_file))
    assert mem_file.exists()
    assert "Land & Soil Profile" in mem_file.read_text(encoding="utf-8")


def test_live_weather_tool():
    from reflex_agent.tools.builtin.live_weather import LiveAgroWeatherTool
    tool = LiveAgroWeatherTool()
    res = tool.execute(location="Indore")
    assert res.success is True
    assert "temperature_celsius" in res.output
    assert "rootzone_soil_moisture_m3m3" in res.output
    assert "pesticide_spray_window_safe" in res.output


def test_gov_schemes_tool():
    from reflex_agent.tools.builtin.gov_schemes import GovtSchemesTool
    tool = GovtSchemesTool()
    res = tool.execute(query="solar pump subsidy kusum")
    assert res.success is True
    assert res.output["matched_scheme"] == "pm_kusum"
    assert "PM-KUSUM" in res.output["scheme_info"]["official_name"]

