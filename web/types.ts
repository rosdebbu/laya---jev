/**
 * KisanZess | TypeScript Type Definitions & State Contracts
 * Fully typed interfaces matching backend Pydantic models for System 1 Laya,
 * System 2 Gemini Vision, Krishi Panchayat WarRoom, and Sarvam AI Indic Speech.
 */

// --- System 1 Laya Reflex Types ---
export type QuestionType = "noul" | "choice" | "score";
export type ProviderType = "auto" | "laya" | "kev" | "jev" | "heuristic" | "mock";
export type AgentMode = "pure_reflex" | "hybrid" | "pure_llm";

export interface Decision<T = string | boolean | number> {
  name: string;
  type: QuestionType;
  value: T;
  confidence: number;
  probabilities?: Record<string, number>;
  raw_response?: unknown;
}

export interface ReflexDecisionResult {
  state: Record<string, unknown> | string;
  decisions: Record<string, Decision>;
  latency_ms: number;
  provider: string;
  model: string;
  tokens_used: number;
  estimated_cost_usd: number;
}

// --- WebSocket Live Stream Step Events ---
export type EventType =
  | "guardrail"
  | "routing"
  | "tool_execution"
  | "synthesis"
  | "complete"
  | "blocked"
  | "error";

export type SystemLevel =
  | "System 1 (Reflex)"
  | "System 1 (Reflex Guardrail)"
  | "System 1 (Reflex Routing)"
  | "System 1 (Reflex Tool Selector)"
  | "System 2 (Reasoning)"
  | "System 2 (Gemini Vision)"
  | "System 2 (Krishi Panchayat)";

export interface AgentStepEvent {
  event_type: EventType;
  system_level: SystemLevel;
  message: string;
  latency_ms: number;
  data: Record<string, unknown>;
}

// --- APMC Mandi Tool Types ---
export interface MandiPriceResult {
  crop: string;
  state: string;
  district: string;
  market_name: string;
  modal_price: string;
  price_range: string;
  msp_declared: string;
  msp_difference: string;
  trend: "BULLISH" | "BEARISH" | "STABLE" | string;
  arrival_quantity_tonnes: number;
  trade_advisory: string;
  last_updated: string;
  source: string;
}

// --- Live Weather & Agro-Meteorology ---
export interface LiveAgroWeatherData {
  location: string;
  state_or_country: string;
  latitude: number;
  longitude: number;
  temperature_celsius: number;
  relative_humidity_pct: number;
  current_rain_mm: number;
  wind_speed_kmh: number;
  soil_surface_temp_c: number;
  rootzone_soil_moisture_m3m3: number;
  soil_moisture_evaluation: string;
  pesticide_spray_window_safe: boolean;
  "3_day_precipitation_forecast_mm": number[];
  rain_probability_pct: number[];
  agri_recommendation: string;
  source: string;
}

// --- Government Schemes & Subsidies ---
export interface SchemeInfo {
  official_name: string;
  objective: string;
  subsidy_details?: string;
  subsidy_percentage?: string;
  disbursement?: string;
  eligibility: string;
  portal: string;
  components?: Record<string, string>;
  premium_rates?: Record<string, string>;
}

export interface GovtSchemeResult {
  matched_scheme: string;
  scheme_info: SchemeInfo;
  all_available_schemes: string[];
}

// --- Krishi Panchayat WarRoom Types ---
export interface PanchayatOpinion {
  agent_role: string;
  agent_title: string;
  perspective: "Biochemical & Pathological" | "Economic & Mandi Arbitrage" | "Soil Ecology & Long-term Yield";
  verdict: string;
  recommended_product: string;
  estimated_cost_inr: number;
  confidence: number;
}

export interface KrishiPanchayatConsensus {
  query: string;
  crop: string;
  opinions: PanchayatOpinion[];
  sarpanch_synthesis_hindi: string;
  sarpanch_synthesis_english: string;
  total_estimated_budget_inr: number;
  economic_viability_score: number;
  prescribed_action_plan: string[];
}

// --- Khet-Vault (Hermes Memory) Types ---
export interface FarmerProfile {
  farmer_id: string;
  name: string;
  district: string;
  state: string;
  land_acres: number;
  soil_type: string;
  soil_ph: number;
  current_crops: string[];
  preferred_mandi: string;
  preferred_language: string;
  disease_history: Array<{
    date: string;
    crop: string;
    diagnosis: string;
    treatment: string;
    status: string;
  }>;
  last_active: string;
}

// --- Sarvam AI Indic Speech Interfaces ---
export interface SarvamTTSRequest {
  text: string;
  language_code?: string;
  speaker?: string;
  pace?: number;
}

export interface SarvamTTSResponse {
  success: boolean;
  provider: "sarvam_ai" | "client_fallback";
  model?: string;
  audio_base64?: string | null;
  language_code: string;
  speaker: string;
  elapsed_ms: number;
  error?: string;
}

export interface SarvamTranslateRequest {
  text: string;
  source_language_code?: string;
  target_language_code?: string;
}

export interface SarvamTranslateResponse {
  success: boolean;
  translated_text: string;
  elapsed_ms?: number;
  error?: string;
}

// --- Telemetry & ROI Protector Metrics ---
export interface TelemetrySummary {
  total_requests: number;
  system_1_ref_count: number;
  system_2_llm_count: number;
  average_latency_ms: number;
  total_tokens_spent: number;
  total_cost_usd: number;
  hypothetical_pure_llm_cost_usd: number;
  cost_savings_pct: number;
  speedup_factor: number;
  attacks_prevented: number;
}
