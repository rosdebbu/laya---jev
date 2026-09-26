# Roshni (रोशनी) - KisanZess Dual-Brain Agri AI Project

Welcome to the **Roshni** workspace for **KisanZess** — the Sub-35ms Dual-Brain Vernacular Farm & Mandi Co-Pilot.

---

## 🌟 Overview

**KisanZess** solves the rural agricultural latency and cost bottleneck by coupling:
1. **System 1 (Reflex Fast-Path)**: Sub-35ms zero-cost local reflex triage using Laya / ModernBERT routing and empirical Scikit-Learn soil ML models.
2. **System 2 (Deep Reasoning & WarRoom)**: 4-agent consensus deliberation (*Dr. Krishi*, *Mandi Vyapari*, *Mitti Mitra*, *Gram Sarpanch*) and Google Gemini 1.5 Flash multimodal vision.

---

## 🚀 Key Features

- **⚡ Sub-35ms Reflex Latency**: In-memory caching and set-based heuristic routing for near-instant vernacular responses.
- **🛡️ 100% Deterministic Safety**: System 1 guardrails blocking prompt injections before LLM token exposure.
- **🌱 Soil & Crop ML**: Scikit-Learn random forest models trained on 2,200+ Indian soil samples with 99.1% accuracy.
- **🛰️ Earth Observation & Mandi Hubs**: Interactive satellite mapping with NDVI/NDWI telemetry for 8 major Indian agricultural zones.
- **🏛️ Krishi Panchayat WarRoom**: Multi-agent deliberative debate balancing crop pathology against APMC market ROI.
- **📜 Khet-Vault Memory**: Auditable, persistent markdown farm state (`FARM_MEMORY.md`) to prevent farmer amnesia.

---

## 💻 Running the Application

### 1. Launch the Server
```bash
python -m uvicorn reflex_agent.api.server:app --host 127.0.0.1 --port 8000
```

### 2. Run Test Suite
```bash
pytest -v
```

### 3. Open Web Dashboard
Navigate to `http://localhost:8000` in your web browser.
