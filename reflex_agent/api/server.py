"""
FastAPI + WebSocket Server for ReflexAgent
Exposes REST APIs and Real-Time WebSocket Streaming for the Glassmorphism Dashboard.
"""

from __future__ import annotations
import os
import sys
import json
import logging
from typing import Dict, Any, Optional

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from reflex_agent.core.engine import DualBrainAgent
from reflex_agent.core.schema import AgentMode
from reflex_agent.benchmarks.comparison import run_benchmark_suite

logger = logging.getLogger("reflex_agent.api")

app = FastAPI(
    title="ReflexAgent API",
    description="Sub-50ms Type-Safe Dual-Brain Agent API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global shared agent instance
agent = DualBrainAgent(mode=AgentMode.HYBRID)


class ChatRequest(BaseModel):
    message: str
    mode: str = "hybrid"


class GuardrailRequest(BaseModel):
    text: str


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "provider": agent.router.active_provider,
        "mode": agent.mode.value,
        "tools_count": len(agent.tools.list_tools()),
    }


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    state = agent.run(req.message)
    return {
        "response": state.final_response,
        "intent": state.current_intent,
        "tool_history": [r.model_dump() for r in state.tool_history],
        "telemetry": agent.get_telemetry_summary().model_dump(),
    }


@app.post("/api/guardrail")
async def guardrail_endpoint(req: GuardrailRequest):
    assessment = agent.guardrail.assess(req.text)
    return assessment.model_dump()


@app.get("/api/tools")
async def tools_endpoint():
    tools = agent.tools.list_tools()
    return [
        {
            "name": t.name,
            "description": t.description,
            "category": t.category,
            "is_destructive": t.is_destructive,
        }
        for t in tools
    ]


@app.get("/api/benchmark")
async def benchmark_endpoint():
    return run_benchmark_suite()


@app.get("/api/telemetry")
async def telemetry_endpoint():
    return agent.get_telemetry_summary().model_dump()


# --- Agricultural Intelligence & ML Studio Endpoints (from l-data-seT---ML) ---
class CropMLRequest(BaseModel):
    N: float = 90.0
    P: float = 42.0
    K: float = 43.0
    temperature: float = 24.0
    humidity: float = 80.0
    ph: float = 6.5
    rainfall: float = 180.0


class FertilizerMLRequest(BaseModel):
    crop: str = "paddy"
    nitrogen: float = 40.0
    phosphorus: float = 20.0
    potassium: float = 30.0


class PanchayatRequest(BaseModel):
    query: str
    crop: str = "Tomato"
    mandi_rate_per_quintal: float = 3800.0
    acreage: float = 4.0


@app.post("/api/ml/crop")
async def crop_ml_endpoint(req: CropMLRequest):
    res = agent.tools.execute_tool(
        "crop_recommendation",
        N=req.N,
        P=req.P,
        K=req.K,
        temperature=req.temperature,
        humidity=req.humidity,
        ph=req.ph,
        rainfall=req.rainfall
    )
    return res.output


@app.post("/api/ml/fertilizer")
async def fertilizer_ml_endpoint(req: FertilizerMLRequest):
    res = agent.tools.execute_tool(
        "fertilizer_prediction",
        crop=req.crop,
        nitrogen=req.nitrogen,
        phosphorus=req.phosphorus,
        potassium=req.potassium
    )
    return res.output


@app.post("/api/panchayat/deliberate")
async def panchayat_endpoint(req: PanchayatRequest):
    from reflex_agent.reasoning.krishi_panchayat import KrishiPanchayatWarRoom
    room = KrishiPanchayatWarRoom()
    consensus = room.deliberate(
        query=req.query,
        crop=req.crop,
        mandi_rate_per_quintal=req.mandi_rate_per_quintal,
        acreage=req.acreage
    )
    return {
        "query": consensus.query,
        "crop": consensus.crop,
        "opinions": [
            {
                "agent_name": op.agent_name,
                "role": op.role,
                "avatar": op.avatar,
                "verdict": op.verdict,
                "key_points": op.key_points,
                "estimated_cost_inr": op.estimated_cost_inr,
                "action_urgency": op.action_urgency
            }
            for op in consensus.opinions
        ],
        "sarpanch_synthesis_hindi": consensus.sarpanch_synthesis_hindi,
        "sarpanch_synthesis_english": consensus.sarpanch_synthesis_english,
        "action_items": consensus.action_items,
        "total_estimated_budget_inr": consensus.total_estimated_budget_inr,
        "economic_viability_score": consensus.economic_viability_score
    }


@app.get("/api/memory/farm")
async def farm_memory_endpoint():
    from reflex_agent.memory.farm_vault import FarmMemoryVault
    vault = FarmMemoryVault()
    profile = vault.get_profile("farmer_001")
    md_content = vault.export_hermes_memory_md("farmer_001")
    return {
        "profile": profile.__dict__ if profile else {},
        "memory_md": md_content,
        "advisories": vault.get_preventive_advisory("farmer_001"),
        "learned_skills": vault.get_learned_skills(profile.district if profile else "Indore")
    }


@app.get("/api/geo/profiles")
async def geo_profiles_endpoint():
    from reflex_agent.tools.builtin.geo_intelligence import LOCATION_PROFILES
    return LOCATION_PROFILES


@app.get("/api/geo/profile/{region}")
async def geo_profile_detail_endpoint(region: str):
    res = agent.tools.execute_tool("geo_intelligence", region=region)
    return res.output


@app.get("/api/weather/live")
async def live_weather_endpoint(location: str = "Indore"):
    res = agent.tools.execute_tool("live_weather", location=location)
    return res.output


@app.get("/api/schemes")
async def gov_schemes_endpoint(query: str = "pm_kisan"):
    res = agent.tools.execute_tool("gov_schemes", query=query)
    return res.output


@app.get("/api/schemes/filter")
async def gov_schemes_filter_endpoint(
    state: Optional[str] = None,
    crop: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
):
    from reflex_agent.tools.builtin.gov_schemes import GovtSchemesTool
    tool = GovtSchemesTool()
    res = tool.execute(query=search or "all", state=state, crop=crop, category=category)
    return res.output


@app.get("/api/schemes/states")
async def gov_schemes_states_endpoint():
    from reflex_agent.tools.builtin.gov_schemes import GovtSchemesTool
    return {"states": GovtSchemesTool.get_available_states()}


@app.get("/api/schemes/crops")
async def gov_schemes_crops_endpoint():
    from reflex_agent.tools.builtin.gov_schemes import GovtSchemesTool
    return {"crops": GovtSchemesTool.get_available_crops()}


# --- Sarvam AI Indic Speech & Language Intelligence ---
class SarvamTTSRequest(BaseModel):
    text: str
    language_code: str = "hi-IN"
    speaker: Optional[str] = None
    pace: float = 1.0


class SarvamTranslateRequest(BaseModel):
    text: str
    source_language_code: str = "en-IN"
    target_language_code: str = "hi-IN"


@app.get("/api/speech/languages")
async def speech_languages_endpoint():
    from reflex_agent.reasoning.sarvam_speech import SUPPORTED_INDIC_LANGUAGES
    return SUPPORTED_INDIC_LANGUAGES


@app.post("/api/speech/tts")
async def sarvam_tts_endpoint(req: SarvamTTSRequest):
    from reflex_agent.reasoning.sarvam_speech import SarvamSpeechEngine
    engine = SarvamSpeechEngine()
    result = engine.text_to_speech(
        text=req.text,
        language_code=req.language_code,
        speaker=req.speaker,
        pace=req.pace,
    )
    return result


@app.post("/api/speech/translate")
async def sarvam_translate_endpoint(req: SarvamTranslateRequest):
    from reflex_agent.reasoning.sarvam_speech import SarvamSpeechEngine
    engine = SarvamSpeechEngine()
    result = engine.translate(
        text=req.text,
        source_language_code=req.source_language_code,
        target_language_code=req.target_language_code,
    )
    return result





@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            user_msg = data.get("message", "")

            # Stream execution events in real time
            for event in agent.run_stream(user_msg):
                await websocket.send_json({
                    "event_type": event.event_type,
                    "system_level": event.system_level,
                    "message": event.message,
                    "latency_ms": event.latency_ms,
                    "data": event.data,
                })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"event_type": "error", "message": str(e)})
        except Exception:
            pass


# Mount Web Dashboard static assets
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../web"))
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/")
    async def index():
        return FileResponse(os.path.join(web_dir, "index.html"))

# Mount Empirical ML Charts from sibling l-data-seT---ML repository
sibling_charts_crop = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "l-data-seT---ML", "output_charts"))
if os.path.exists(sibling_charts_crop):
    app.mount("/charts/crop", StaticFiles(directory=sibling_charts_crop), name="charts_crop")

sibling_charts_fert = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "l-data-seT---ML", "output_charts_fertilizer"))
if os.path.exists(sibling_charts_fert):
    app.mount("/charts/fertilizer", StaticFiles(directory=sibling_charts_fert), name="charts_fertilizer")
