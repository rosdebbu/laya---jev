"""
Example 03: Multilingual Reflex Routing
Demonstrates intent detection across Spanish, French, German, and Hindi
without costly translation prompts.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reflex_agent.core.router import ReflexRouter
from reflex_agent.core.schema import ChoiceQuestion

MULTILINGUAL_INPUTS = [
    {"lang": "Spanish", "text": "¿Cómo puedo restablecer mi contraseña de inicio de sesión?"},
    {"lang": "French", "text": "J'ai été facturé deux fois pour mon abonnement mensuel."},
    {"lang": "German", "text": "Gibt es eine API-Dokumentation für Python und Node.js?"},
    {"lang": "Hindi", "text": "मुझे अपने खाते में लॉग इन करने में समस्या आ रही है।"},
]

ROUTING_QUESTION = {
    "intent": ChoiceQuestion(
        instructions="What is the user's intent?",
        criteria={
            "account_access": "Login, password reset, account recovery, authentication problems",
            "billing": "Double charge, invoices, subscription payment",
            "technical_docs": "API documentation, code examples, SDK guides",
            "general_inquiry": "General questions or casual chat",
        },
    )
}

def main():
    print("=" * 70)
    print("🌐 MULTILINGUAL INTENT ROUTING DEMO")
    print("=" * 70)

    router = ReflexRouter()

    for item in MULTILINGUAL_INPUTS:
        result = router.decide(state={"text": item["text"]}, questions=ROUTING_QUESTION)
        intent = result.get_choice("intent")
        conf = result.get_confidence("intent")

        print(f"[{item['lang']}] \"{item['text']}\"")
        print(f"  ▸ Intent:     {intent.upper()}")
        print(f"  ▸ Confidence: {conf:.2f}")
        print(f"  ▸ Latency:    {result.latency_ms:.2f} ms\n")

if __name__ == "__main__":
    main()
