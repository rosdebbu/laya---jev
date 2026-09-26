# Roshni Changelog

## [1.3.0] - 2026-09-27

### UI/UX & Interaction Enhancements
- **Vertical Krishi Varta Slide-Out Drawer**: Relocated the Krishi Varta chat console to a right-hand slide-out drawer with a vertical handle tab that moves aside alongside the drawer during expansion/collapse.
- **Dark & Light Mode Integration**: Added explicit `🌑 Dark Mode` and `☀️ Light Mode` options to the Circadian Mode dropdown selector with persistent local storage.
- **Scrollable Segmented Navigation Bar**: Formatted the top navigation bar into a horizontally scrollable segmented control for Soil ML, Krishi Panchayat, Khet-Vault Memory, and Dual-Brain Telemetry.
- **Expandable Header Control Stack**: Shifted header controls (Audio, Benchmark, Mode) into an expandable vertical stack with hover tooltips and glow effects.

---

## [1.2.0] - 2026-09-27

### UI/UX Updates
- Restored the active UI to the user's preferred layout featuring the APMC mini-ticker, dedicated 4-tab bar, 4-chip Crisis Action ribbon, and multi-card Telemetry & ROI dashboard.
- Maintained high-contrast Outdoor Sunlight Field Mode for rural field usage.

### Performance & Latency
- Validated sub-35ms pipeline with zero-cost reflex routing and in-memory APMC caching.
- Verified 15/15 unit and integration test suite passing.

---

## [1.1.0] - 2026-09-26

### Features
- Added `Roshni` workspace directory with project guides.
- Implemented single-pass System 1 evaluation in `reflex_agent/core/engine.py`.
- Optimized Random Forest crop models in `reflex_agent/tools/builtin/agri_ml.py`.

---

## [1.0.0] - 2026-09-26

### Initial Release
- Initial Dual-Brain architecture combining Laya ModernBERT System 1 reflex and OpenZess Krishi Panchayat multi-agent consensus.
