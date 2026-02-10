"""
Test script to verify AI provider switching works
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.ai_config import AIConfig, AIProvider

def test_provider_switching():
    print("=" * 60)
    print("AI PROVIDER SWITCHING TEST")
    print("=" * 60)

    # Show initial state
    print("\n[1] Initial Configuration:")
    print(f"   Active Provider: {AIConfig.ACTIVE_PROVIDER.value}")
    print(f"   Fallback Provider: {AIConfig.FALLBACK_PROVIDER.value}")

    # Check provider status
    info = AIConfig.get_provider_info()
    print("\n[2] Provider Status:")
    for provider, status in info['providers_status'].items():
        icon = "[OK]" if status else "[X]"
        print(f"   {icon} {provider.upper()}")

    # Test switching
    print("\n[3] Testing Provider Switching:")

    # Try switching to Gemini
    print("\n   Switching to GEMINI...")
    if AIConfig.switch_provider(AIProvider.GEMINI):
        print(f"   [SUCCESS] Now using: {AIConfig.ACTIVE_PROVIDER.value}")
    else:
        print("   [FAILED] Gemini not configured")

    # Try switching to Hugging Face
    print("\n   Switching to HUGGING FACE...")
    if AIConfig.switch_provider(AIProvider.HUGGINGFACE):
        print(f"   [SUCCESS] Now using: {AIConfig.ACTIVE_PROVIDER.value}")
    else:
        print("   [FAILED] Hugging Face not configured")

    # Try switching to Local
    print("\n   Switching to LOCAL...")
    if AIConfig.switch_provider(AIProvider.LOCAL):
        print(f"   [SUCCESS] Now using: {AIConfig.ACTIVE_PROVIDER.value}")
    else:
        print("   [FAILED] Local model not found")

    # Try switching to OpenAI
    print("\n   Switching to OPENAI...")
    if AIConfig.switch_provider(AIProvider.OPENAI):
        print(f"   [SUCCESS] Now using: {AIConfig.ACTIVE_PROVIDER.value}")
    else:
        print("   [FAILED] OpenAI not configured")

    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

    print("\nFinal Configuration:")
    print(f"   Active Provider: {AIConfig.ACTIVE_PROVIDER.value}")

    print("\nTo switch providers:")
    print("   1. Edit backend/config/ai_config.py")
    print("   2. Or use API: POST /api/ai/switch-provider")
    print("      Body: {\"provider\": \"gemini\"}")

if __name__ == "__main__":
    test_provider_switching()
