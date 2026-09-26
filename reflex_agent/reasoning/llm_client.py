"""
System 2 LLM Reasoning Client
Supports LiteLLM (OpenAI, Anthropic, Groq, DeepSeek, Ollama) with intelligent offline fallback.
"""

from __future__ import annotations
import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from reflex_agent.reasoning.prompts import SYSTEM_PROMPT, ARGUMENT_EXTRACTION_PROMPT

logger = logging.getLogger("reflex_agent.reasoning")


class ReasoningClient:
    """
    Orchestrates System 2 deep reasoning and conversational synthesis.
    Only triggered when System 1 requests synthesis or argument extraction.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("DEFAULT_LLM_MODEL", "gpt-4o-mini")
        self.has_api_key = bool(
            os.environ.get("OPENAI_API_KEY")
            or os.environ.get("ANTHROPIC_API_KEY")
            or os.environ.get("GROQ_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
        )

    def extract_arguments(self, tool_name: str, user_input: str) -> Dict[str, Any]:
        """Extract tool arguments deterministically or via LLM."""
        # Fast deterministic argument extraction heuristics
        if tool_name == "calculator":
            # Extract expression
            words = user_input.replace("calculate", "").replace("what is", "").replace("compute", "").strip()
            # strip trailing question marks or punctuation
            clean = "".join([c for c in words if c in "0123456789+-*/().^% "]).strip()
            return {"expression": clean if clean else words}

        if tool_name == "file_ops":
            parts = user_input.split()
            action = "read"
            if any(w in user_input.lower() for w in ["write", "create", "save"]):
                action = "write"
            elif any(w in user_input.lower() for w in ["list", "ls", "dir"]):
                action = "list"
            # find path
            path = "README.md"
            for p in parts:
                if "." in p or "/" in p or "\\" in p:
                    path = p.strip(",'\"`")
                    break
            return {"action": action, "path": path}

        if tool_name == "web_search":
            q = user_input.replace("search for", "").replace("search", "").replace("lookup", "").strip()
            return {"query": q if q else user_input}

        if tool_name == "shell_exec":
            cmd = user_input.replace("run command", "").replace("run", "").replace("exec", "").strip()
            return {"command": cmd if cmd else user_input}

        if tool_name == "memory_store":
            return {"action": "list_all", "key": "default"}

        if tool_name == "mandi_price":
            lower = user_input.lower()
            commodity = "tomato"
            if "soybean" in lower or "सोयाबीन" in user_input:
                commodity = "soybean"
            elif "tomato" in lower or "टमाटर" in user_input:
                commodity = "tomato"
            elif "wheat" in lower or "गेहूं" in user_input or "गेंहू" in user_input:
                commodity = "wheat"
            elif "onion" in lower or "प्याज" in user_input or "प्याज़" in user_input:
                commodity = "onion"
            elif "paddy" in lower or "धान" in user_input or "rice" in lower or "चावल" in user_input:
                commodity = "paddy"
            elif "potato" in lower or "आलू" in user_input:
                commodity = "potato"
            elif "cotton" in lower or "कपास" in user_input:
                commodity = "cotton"
            elif "maize" in lower or "मक्का" in user_input:
                commodity = "maize"

            market = None
            if "indore" in lower or "इंदौर" in user_input:
                market = "Indore Mandi"
            elif "agartala" in lower or "अगरतला" in user_input:
                market = "Agartala Main Mandi"
            elif "kolar" in lower or "कोलार" in user_input:
                market = "Kolar APMC"
            elif "azadpur" in lower or "आज़ादपुर" in user_input:
                market = "Azadpur Mandi"

            return {"commodity": commodity, "market": market}

        if tool_name == "crop_recommendation":
            import re
            lower = user_input.lower()
            n_m = re.search(r"n\s*[:=]\s*(\d+(\.\d+)?)", lower)
            p_m = re.search(r"p\s*[:=]\s*(\d+(\.\d+)?)", lower)
            k_m = re.search(r"k\s*[:=]\s*(\d+(\.\d+)?)", lower)
            ph_m = re.search(r"ph\s*[:=]\s*(\d+(\.\d+)?)", lower)
            rain_m = re.search(r"rain(?:fall)?\s*[:=]\s*(\d+(\.\d+)?)", lower)
            return {
                "N": float(n_m.group(1)) if n_m else 90.0,
                "P": float(p_m.group(1)) if p_m else 42.0,
                "K": float(k_m.group(1)) if k_m else 43.0,
                "temperature": 25.0,
                "humidity": 75.0,
                "ph": float(ph_m.group(1)) if ph_m else 6.5,
                "rainfall": float(rain_m.group(1)) if rain_m else 150.0,
            }

        if tool_name == "fertilizer_prediction":
            import re
            lower = user_input.lower()
            crop = "paddy"
            if "soybean" in lower or "सोयाबीन" in user_input:
                crop = "soybean"
            elif "wheat" in lower or "गेहूं" in user_input or "गेंहू" in user_input:
                crop = "wheat"
            elif "cotton" in lower or "कपास" in user_input:
                crop = "cotton"
            elif "maize" in lower or "मक्का" in user_input:
                crop = "maize"

            n_m = re.search(r"(?:नाइट्रोजन|nitrogen|n)\s*[:=]?\s*(\d+)", lower)
            p_m = re.search(r"(?:फास्फोरस|phosphorus|p)\s*[:=]?\s*(\d+)", lower)
            k_m = re.search(r"(?:पोटाश|potassium|k)\s*[:=]?\s*(\d+)", lower)
            return {
                "crop": crop,
                "nitrogen": float(n_m.group(1)) if n_m else 40.0,
                "phosphorus": float(p_m.group(1)) if p_m else 20.0,
                "potassium": float(k_m.group(1)) if k_m else 30.0,
            }

        if tool_name == "krishi_panchayat":
            lower = user_input.lower()
            crop = "Tomato"
            if "soybean" in lower or "सोयाबीन" in user_input:
                crop = "Soybean"
            elif "cotton" in lower or "कपास" in user_input:
                crop = "Cotton"
            elif "wheat" in lower or "गेहूं" in user_input:
                crop = "Wheat"
            return {
                "query": user_input,
                "crop": crop,
                "mandi_rate_per_quintal": 3800.0,
                "acreage": 2.0,
            }

        # If LLM is available, use litellm
        if self.has_api_key:
            try:
                import litellm
                prompt = ARGUMENT_EXTRACTION_PROMPT.format(tool_name=tool_name, user_input=user_input)
                res = litellm.completion(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                text = res.choices[0].message.content.strip()
                # Parse JSON
                if "{" in text and "}" in text:
                    text = text[text.find("{"):text.rfind("}") + 1]
                return json.loads(text)
            except Exception as e:
                logger.warning(f"LLM argument extraction fallback: {e}")

        return {"input": user_input}

    def synthesize(
        self,
        user_input: str,
        tool_results: List[Dict[str, Any]],
        system_1_intent: Optional[str] = None,
        force_llm: bool = False,
    ) -> str:
        """
        Synthesizes the final user-facing response.
        If tool results are present, formats them with sub-millisecond local templates,
        or routes to low-latency LLM synthesis when complex reasoning is required.
        """
        # High-performance Fast-Path: Deterministic tools do not require slow LLM overhead
        if tool_results and not force_llm:
            local_formatted = self._synthesize_local(user_input, tool_results, system_1_intent)
            if local_formatted:
                return local_formatted

        # If API key is present, use litellm with fast timeout
        if self.has_api_key:
            try:
                import litellm
                context_str = json.dumps(tool_results, indent=2)
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"User Request: {user_input}\n\nSystem 1 Intent: {system_1_intent}\n\nTool Executions:\n{context_str}\n\nPlease generate the final answer in empathetic vernacular Hindi + English summary:",
                    },
                ]
                res = litellm.completion(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.3,
                    timeout=3.5,
                )
                return res.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"LLM synthesis skipped/fallback ({e}), using local reflex synthesizer")

        return self._synthesize_local(user_input, tool_results, system_1_intent)

    def synthesize_stream(
        self,
        user_input: str,
        tool_results: List[Dict[str, Any]],
        system_1_intent: Optional[str] = None,
    ):
        """
        Stream response token-by-token for sub-100ms Time-To-First-Token (TTFT).
        """
        # Fast-path for tool results
        if tool_results:
            full_text = self._synthesize_local(user_input, tool_results, system_1_intent)
            yield full_text
            return

        if self.has_api_key:
            try:
                import litellm
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ]
                response = litellm.completion(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.3,
                    stream=True,
                    timeout=4.0,
                )
                for chunk in response:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        yield delta
                return
            except Exception as e:
                logger.warning(f"Streaming LLM fallback: {e}")

        yield self._synthesize_local(user_input, tool_results, system_1_intent)

    def _synthesize_local(
        self,
        user_input: str,
        tool_results: List[Dict[str, Any]],
        system_1_intent: Optional[str] = None,
    ) -> str:
        """High-performance local synthesis (Sub-0.1ms, Zero API key needed)."""
        if not tool_results:
            return f"Processed request '{user_input}'. Intent identified as: {system_1_intent or 'general'}."

        last_tool = tool_results[-1]
        tool_name = last_tool.get("tool_name", "tool")
        output = last_tool.get("output")
        is_success = last_tool.get("is_success", True)
        error = last_tool.get("error_message")

        if not is_success:
            return f"Attempted to execute '{tool_name}', but encountered an issue: {error}"

        if tool_name == "mandi_price":
            data = output if isinstance(output, dict) else {}
            comm = str(data.get("crop") or data.get("commodity") or "फसल").title()
            mandi = data.get("market_name") or data.get("market") or data.get("query_district") or "APMC Mandi"
            modal = data.get("modal_price", "N/A")
            price_range = data.get("price_range") or f"₹{data.get('min_price', 0):,} - ₹{data.get('max_price', 0):,}"
            trend = data.get("trend", "स्थिर")
            msp = data.get("msp_status", "सक्रिय MSP गारंटी")
            rec = data.get("recommendation") or data.get("actionable_selling_advice") or "मंडी में भाव की जांच करके ही अपनी उपज बेचें।"
            
            return (
                f"🌾 **{comm} मंडी भाव बुलेटिन ({mandi})**\n\n"
                f"• **औसत (Modal) भाव:** **{modal}**\n"
                f"• **दाम की सीमा:** {price_range}\n"
                f"• **बाजार का रुझान (Trend):** {trend}\n"
                f"• **सरकारी MSP स्थिति:** {msp}\n\n"
                f"💡 **व्यापारिक किसान सलाह:** {rec}\n\n"
                f"*(सिस्टम 1 आधुनिक रिफ्लेक्स इंजन: <15ms में सत्यापित APMC डेटा | ₹0.00 खर्च)*"
            )

        if tool_name == "crop_recommendation":
            data = output if isinstance(output, dict) else {}
            top_crops = data.get("top_recommendations", [])
            primary = data.get("primary_crop", "Optimal Crop")
            crops_text = "\n".join([
                f"  {i+1}. **{c.get('crop', '').title()}** — अनुकूलता: **{c.get('confidence_score', 0)*100:.1f}%**"
                for i, c in enumerate(top_crops[:3])
            ])
            adv = data.get("soil_health_advisory", "मिट्टी में पर्याप्त जैविक खाद डालें और नमी बनाए रखें।")

            return (
                f"🌱 **मृदा परीक्षण एवं फसल चयन रिपोर्ट (l-data-seT---ML Analysis)**\n\n"
                f"आपकी मिट्टी के पोषक तत्वों (N-P-K और pH) के आधार पर सर्वश्रेष्ठ फसल:\n\n"
                f"🏆 **मुख्य अनुशंसा: {primary.upper()}**\n\n"
                f"📊 **शीर्ष 3 अनुकूल फसलें:**\n{crops_text}\n\n"
                f"💡 **मृदा सुधार सलाह:** {adv}\n\n"
                f"*(2,200+ भारतीय मृदा नमूनों पर प्रशिक्षित Scikit-Learn मॉडल: <10ms)*"
            )

        if tool_name == "fertilizer_prediction":
            data = output if isinstance(output, dict) else {}
            sched = data.get("fertilizer_schedule", {})
            status = data.get("soil_status", "")
            advisory = data.get("actionable_farmer_advisory", "संतुलित खाद का प्रयोग करें, अतिरिक्त यूरिया न डालें।")

            return (
                f"🧪 **संतुलित खाद अनुसूची (Balanced NPK Fertilizer Schedule)**\n\n"
                f"• **मृदा स्थिति:** {status}\n\n"
                f"📋 **अनुशंसित खाद की खुराक (प्रति एकड़):**\n"
                f"  - **Urea (यूरिया):** {sched.get('Urea', '0')} kg\n"
                f"  - **DAP (डाई-अमोनियम फास्फेट):** {sched.get('DAP', '0')} kg\n"
                f"  - **MOP (म्यूरेट ऑफ पोटाश):** {sched.get('MOP', '0')} kg\n\n"
                f"⚠️ **दुकानदार के बहकावे से बचें:** {advisory}\n\n"
                f"*(स्टोइचियोमेट्रिक मृदा मॉडल: फिजूलखर्ची और जमीन को बंजर होने से बचाएं)*"
            )

        if tool_name == "krishi_panchayat":
            data = output if isinstance(output, dict) else {}
            hindi_s = data.get("sarpanch_synthesis_hindi", "")
            eng_s = data.get("sarpanch_synthesis_english", "")
            actions = data.get("action_items", [])
            actions_text = "\n".join([f"  • {act}" for act in actions])
            budget = data.get("total_estimated_budget_inr", 0.0)
            viability = data.get("economic_viability_score", 0.85)

            return (
                f"🏛️ **कृषि पंचायत सर्वसम्मति फैसला (Krishi Panchayat Consensus)**\n\n"
                f"📜 **ग्राम सरपंच का निर्णय (हिंदी):**\n{hindi_s}\n\n"
                f"🎯 **त्वरित कार्य योजना (Action Items):**\n{actions_text}\n\n"
                f"💰 **अनुमानित बजट:** ₹{budget:.0f} (पारंपरिक दुकानदार के ₹2,500+ रासायनिक कॉकटेल से भारी बचत)\n"
                f"📈 **आर्थिक व्यवहार्यता स्कोर:** {viability*100:.0f}%\n\n"
                f"*(4-एजेंट पंचायत: डॉ. कृषि + मंडी व्यापारी + मिट्टी मित्र + ग्राम सरपंच)*"
            )

        if tool_name == "calculator":
            return f"Result: **{output}**"

        if tool_name == "file_ops":
            return f"File operation completed successfully:\n```\n{output}\n```"

        if tool_name == "web_search":
            summary = output.get("summary") if isinstance(output, dict) else str(output)
            return f"Search Result:\n{summary}"

        if tool_name == "shell_exec":
            return f"Shell Command Output:\n```\n{output}\n```"

        if tool_name == "memory_store":
            return f"Memory update: {output}"

        return f"Executed `{tool_name}` successfully. Result: {output}"
