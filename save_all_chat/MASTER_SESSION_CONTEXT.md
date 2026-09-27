# 🌾 KisanZess — Master Project Context & Session Knowledge Base

> **Note for Future AI Agents & Developers:**  
> This file contains the complete, authoritative record of all strategic decisions, user requirements, UI/UX specifications, architectural designs, color palettes, and code changes made in this repository. Read this file before proposing or executing further changes to maintain continuity.

---

## 📌 1. Project Overview & Objective

| Field | Detail |
| :--- | :--- |
| **Project Name** | **KisanZess: Dual-Brain Vernacular Farm & Mandi Co-Pilot** |
| **Repository** | `https://github.com/rosdebbu/laya---jev` |
| **Target Event** | **Build with AI: Code for Communities (Second Edition)** on [Hack2skill](https://hack2skill.com/event/codeforcommunities2) |
| **Track** | **Track 4: Agricultural Intelligence** |
| **Organizers** | Google Cloud & Google Developer Groups (GDG India) |
| **Core Innovation** | Daniel Kahneman's **Dual-Brain Architecture**: System 1 Reflex (<35ms, $0 token cost) + System 2 Multimodal Reasoning (Google Gemini 1.5 Flash Vision & Voice). |

---

## 🎯 2. Core Real-World Problems Solved

1. **APMC Mandi Price Opacity & Distress Sales:**
   * Farmers travel 40+ km to local mandis without price intelligence and are forced to sell 30–50% below fair market value.
   * *Solution:* **"Zepto-Style" Mandi Arbitrage Engine** comparing 3 nearest APMC mandis within a 50 km radius, deducting transport/diesel costs, and highlighting the **Net Extra Cash Profit** (e.g. `+₹4,720 Net Profit`). Includes an **MSP Defense Alert** if local trader rates fall below government Minimum Support Price.

2. **Token Explosion on Government Portals:**
   * Traditional LLMs choke on 20,000+ words of legal/HTML junk on government websites (`pmkisan.gov.in`, `agrimachinery.nic.in`), causing high cloud bills, latency, and hallucinations.
   * *Solution:* **Laya System 1 Zero-Token Scheme Harvester**. Laya's ModernBERT classifier prunes bureaucratic noise in sub-35ms, extracts structured scheme criteria (State, Crop, Land ceiling, Subsidy %), and generates 1-click **Farmer Action Cards** (e.g. $4 \text{ acres} \times ₹7,000 = \mathbf{₹28,000}$ cash incentive).

3. **Chemical Overdose & Chatbot Hallucinations:**
   * Standard generative chatbots hallucinate dangerous chemical pesticide dosages that poison soil and put farmers into debt.
   * *Solution:* **Deterministic Scikit-Learn ML models** trained on Indian agricultural data for 22 crops and stoichiometric NPK fertilizer deficits. Governed by a **4-Agent Krishi Panchayat** (Dr. Krishi, Mandi Vyapari, Mitti Mitra, Gram Sarpanch).

4. **Rural Phone Screen Glare in Open Fields:**
   * Dark mode glassmorphism turns into a black mirror reflecting direct mid-day sunlight, making text unreadable on dusty, smudged smartphone screens.
   * *Solution:* **Dual-Display System**:
     * *Mode A (Indoor/Laptop):* Luxury Dark Forest Green palette.
     * *Mode B (Outdoor/Phone):* 1-Tap **☀️ Anti-Glare Sunlight Mode** (`#F4F7F4` matte canvas, stark `#011207` jet-black text with 16:1 WCAG AAA contrast, solid 2px borders) + **"Eyes-Free" Vernacular Audio Readout Bar**.

5. **Frictionless Onboarding:**
   * *Solution:* **1-Tap Auto-Location Diagnostic** (GPS / Pincode) that auto-locks State, District, ICAR Agro-Climatic Zone, soil baseline, 3 nearest mandis, and local KVK pest advisories in under 50ms.

---

## 🎨 3. UI/UX System & Color Tokens

Inspired by premium luxury earth and forest palettes:

### Luxury Forest Palette Tokens:
* **Near-Black Green (Main Canvas):** `#011207`
* **Dark Evergreen (Sub-surface):** `#013220`
* **Deep Forest Roast (Frosted Glass):** `#1A3636` / `#40534C`
* **Emerald Green (Primary Action & Gains):** `#50C878` / `#0B6E4F`
* **Apple Green (Interactive Badges):** `#8BC53D`
* **Soft Sage Mint (Highlight Cards):** `#E2F0CC`
* **Mint Whisper (Sub-labels):** `#D1F2EB`
* **Almond Gold (Secondary Badges & Alerts):** `#D6BD98`

### Anti-Glare Sunlight Mode Tokens:
* **Matte Outdoor Base:** `#F4F7F4` / `#FFFFFF`
* **High-Contrast Jet Black Typography:** `#011207` (16:1 contrast ratio)
* **Solid Matte Borders:** 2px solid `#013220` (zero blur, zero transparency wash-out)

---

## 📂 4. ChatGPT-Style Slide-Out Sidebar Architecture

The UI features a left-side drawer accessible via the `☰` hamburger button or `Ctrl + /`:

```text
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│  🌾 KisanZess        [✕]  │ 🌾 KisanZess | Dual-Brain Agri Co-Pilot                │
│                           │                                                        │
│  [ + New Consultation ]   │  ( Main Chat & Agricultural Intelligence Screen )      │
│                           │                                                        │
│ ┌───────────────────────┐ │                                                        │
│ │ 👨‍🌾 Rameshwar Patel   │ │                                                        │
│ │ 4.0 Acres Black Soil  │ │                                                        │
│ │ Indore APMC • Cotton  │ │                                                        │
│ │ 🧠 Khet-Vault Active  │ │                                                        │
│ └───────────────────────┘ │                                                        │
│                           │                                                        │
│ 🌟 FEATURE SHOWCASE       │                                                        │
│                           │                                                        │
│ 📈 Mandi Arbitrage Hub    │                                                        │
│ 🏛️ Govt Scheme Harvester │                                                        │
│ 📸 Gemini Leaf Vision     │                                                        │
│ 🌱 Soil NPK & Fertilizer  │                                                        │
│ ⚖️ Krishi Panchayat      │                                                        │
│ 🌦️ Live Agro-Weather      │                                                        │
│                           │                                                        │
│ ───────────────────────── │                                                        │
│ ⚡ SYSTEM 1 STATUS        │                                                        │
│ Provider: Local Laya      │                                                        │
│ Latency:  <35ms (18.4ms)  │                                                        │
│ Savings:  97.3% ($0 cost) │                                                        │
│                           │                                                        │
│ [ ☀️ Sunlight Field Mode] │                                                        │
│ [ 🌐 Language: English  ] │                                                        │
│ [ ⚙️ Edit Farm Profile  ] │                                                        │
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 🛠️ 5. Codebase Changes Implemented in this Session

### 1. Obsolete Files Cleaned:
* Cleaned and removed obsolete scratch script [`scratch_clean.py`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/scratch_clean.py).

### 2. `web/index.html` (Exact Alignment with Master Mockup `imageproject/kisanzess_dashboard_mockup_1790538705529.jpg`):
* Integrated unified `.dashboard-frame` container pairing the Desktop Left Sidebar (`#app-sidebar`) and Main Dashboard (`.app-main-content`).
* Added Left Sidebar with:
  * Brand Row: Sprout `🌾 KisanZess` + `<<` collapse button (`#btn-sidebar-collapse`).
  * Section 1: `+ New Consultation` (`#btn-new-consultation`) action button.
  * Farmer Context Card: Rameshwar Patel • 4.0 Acres • Indore.
  * 5 Nav Items: `Mandi Arbitrage Hub`, `Govt Schemes Harvester`, `Gemini Leaf Vision`, `Soil NPK Studio`, `Krishi Panchayat`.
  * Bottom Dock: `Laya System 1: 18ms` telemetry pill and 1-tap Anti-Glare Sunlight toggle.
* Main Content Area:
  * Top Dashboard Bar: `Dashboard` title, Indic language selector, 1-tap Field Mode button, notification bell with live pulse dot, farmer profile avatar.
  * Top Ticker Row: `Live APMC mandi Ticker` with green badges (`▲ ₹251.00`, `▲ ₹1,170.00`, `▲ ₹780.00`, etc.) and `📍 Indore & Malwa (Auto-Detected) [Zone VIII]`.
  * Top Mode Status Bar: 1-Tap `☀️ Anti-Glare Sunlight Mode` (`ACTIVE`/`STANDBY`), `🔆 Auto-Light Sensor` (45k Lux), `🔊 'Eyes-Free' Audio Readout` with live animated sound waves.
  * Hero Grid (`.dashboard-hero-grid`):
    * **Left: Mandi Arbitrage comparison (3 Columns)**:
      * Dewas Mandi (Local, 5 km).
      * Ujjain Mandi (Best-Return Centerpiece in solid **Light Sage Mint Canvas `#E2F0CC`** with deep evergreen typography and `+₹4,720 Net Profit`).
      * Indore Mandi (Alternate, 35 km).
      * Bottom progress / track slider indicator.
      * Crop switcher dropdown (`#select-arbitrage-crop`: Soybean, Wheat, Cotton, Tomato, Onion).
    * **Right: Stacked Intelligence Cards**:
      * `Government Scheme` card with 1-click `Action Scheme` button.
      * `Conversational AI` card with live audio wave animation, vernacular speech bubble, quick audio/panchayat buttons, and inline prompt input (`#hero-user-input`).

### 3. `web/style.css`:
* Added `.dashboard-frame` flex layout with responsive collapse for desktop and drawer slide-in for mobile.
* Styled `.best-return-card` with solid `#E2F0CC` canvas, 16:1 contrast text, and vibrant emerald button (`#50C878`).
* Styled `.arbitrage-track-bar`, `.conversational-hero-input`, `.sidebar-nav-item.active`, `.btn-new-consultation`.
* Preserved complete WCAG AAA high-contrast overrides under `body.field-mode`.

### 4. `web/app.js`:
* Wired desktop sidebar collapse (`#btn-sidebar-collapse`) and mobile drawer toggle (`#btn-sidebar-toggle`).
* Implemented `startNewConsultation()` to clear chat history, restore initial welcome state, and announce audio greeting.
* Implemented dynamic multi-mandi arbitrage calculation across 5 crops (Soybean, Wheat, Cotton, Tomato, Onion).
* Connected `Action Scheme` to switch to `tab-schemes`.
* Connected `🔊 Listen (Audio)` to Web Speech API for vernacular voice playback.
* Connected inline hero input to dispatch queries directly to Laya System 1 reflex or Krishi Panchayat.

### 5. `reflex_agent/tools/builtin/mandi_tool.py`:
* Added `soybean` market intelligence profile for Malwa Plateau.
* Added `calculate_arbitrage()` classmethod computing multi-mandi gross, transport diesel deduction, and net extra cash profit.

---

## 🗺️ 6. Master Phased Implementation Roadmap

* **Phase 1: UI & Responsive Anti-Glare System** *(COMPLETED)*
  * [x] ChatGPT-style Drawer Sidebar & Desktop Frame (Exact match to Mockup).
  * [x] Dual-Display Anti-Glare Mode (Sunlight vs. Indoors).
  * [x] Top Mode Status Indicators (Anti-Glare, Auto-Light Sensor, Eyes-Free Audio).
  * [x] Centerpiece Light Sage Mint Card 2 (`#E2F0CC`).
* **Phase 2: Backend Engines & Data Pipelines** *(COMPLETED)*
  * [x] "Zepto-Style" Mandi Arbitrage calculation service in `mandi_tool.py`.
  * [x] Dynamic crop switching and live arbitrage recalculation in `app.js`.
  * [x] Laya Government Scheme Harvester 1-click action linkage.
* **Phase 3: Integration & End-to-End Verification** *(READY FOR LOCAL TESTING)*
  * [x] Obsolete scratch files cleaned (`scratch_clean.py`).
  * [ ] Local execution test via `run_kisanzess.bat` (Option `2`).
  * [ ] Mobile viewport validation.
* **Phase 4: Hack2skill Submission & Video**
  * [ ] Record 3-minute pitch video following the script.
  * [ ] Upload presentation deck (`Comprehensive_Viva_Crop_Fertilizer_ML.pptx`).
  * [ ] Submit to Hack2skill Code for Communities 2.0 portal.

---

## 📁 7. Key File Locations & Assets

* **Launch Script:** [`run_kisanzess.bat`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/run_kisanzess.bat)
* **Web Frontend:** 
  * HTML: [`web/index.html`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/web/index.html)
  * CSS: [`web/style.css`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/web/style.css)
  * JS: [`web/app.js`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/web/app.js)
* **Backend Core & Tools:**
  * Mandi Tool: [`reflex_agent/tools/builtin/mandi_tool.py`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/reflex_agent/tools/builtin/mandi_tool.py)
  * Schemes Tool: [`reflex_agent/tools/builtin/gov_schemes.py`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/reflex_agent/tools/builtin/gov_schemes.py)
  * Router: [`reflex_agent/core/router.py`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/reflex_agent/core/router.py)
* **Master Image Assets:**
  * Desktop Hero Mockup: [`imageproject/kisanzess_dashboard_mockup_1790538705529.jpg`](file:///c:/Users/ROSHNI/OneDrive/Documents/GitHub/laya---jev/imageproject/kisanzess_dashboard_mockup_1790538705529.jpg)
  * Visual Showcase Gallery: [`kisanzess_ui_showcase.md`](file:///C:/Users/ROSHNI/.gemini/antigravity-ide/brain/04cf7ad6-fbab-48f9-8d96-689f47e0ffa3/kisanzess_ui_showcase.md)
