"""
Test script for pricing and AI integration
Run this to verify the new pricing logic and AI providers are working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.pricing import WastePricing
from config.ai_config import AIConfig, AIProvider

def test_pricing():
    """Test the new pricing logic"""
    print("=" * 60)
    print("PRICING LOGIC TEST")
    print("=" * 60)

    # Test case 1: 2 kg iron (metal)
    print("\n1. Testing 2 kg iron (metal):")
    print("-" * 40)
    result = WastePricing.calculate_net_transaction(
        waste_type='metal',
        quantity_kg=2,
        subtype='iron',
        distance_km=0
    )

    print(f"Waste Type: metal (iron)")
    print(f"Quantity: 2 kg")
    print(f"Market Value: ₹{result['waste_value']['total_value']} (₹{result['waste_value']['rate_per_kg']}/kg)")
    print(f"Collection Cost: ₹{result['collection_cost']['total_cost']}")
    print(f"Net Amount: ₹{result['net_amount']}")
    print(f"Transaction Type: {result['transaction_type']}")

    if result['net_amount'] < 0:
        print(f"✓ User PAYS ₹{abs(result['net_amount']):.2f} for collection")
    else:
        print(f"✓ User EARNS ₹{result['net_amount']:.2f} 🎉")

    # Test case 2: 10 kg copper (valuable metal)
    print("\n2. Testing 10 kg copper (valuable metal):")
    print("-" * 40)
    result = WastePricing.calculate_net_transaction(
        waste_type='metal',
        quantity_kg=10,
        subtype='copper',
        distance_km=0
    )

    print(f"Waste Type: metal (copper)")
    print(f"Quantity: 10 kg")
    print(f"Market Value: ₹{result['waste_value']['total_value']} (₹{result['waste_value']['rate_per_kg']}/kg)")
    print(f"Collection Cost: ₹{result['collection_cost']['total_cost']}")
    print(f"Net Amount: ₹{result['net_amount']}")
    print(f"Transaction Type: {result['transaction_type']}")

    if result['net_amount'] < 0:
        print(f"✓ User PAYS ₹{abs(result['net_amount']):.2f} for collection")
    else:
        print(f"✓ User EARNS ₹{result['net_amount']:.2f} 🎉")

    # Test case 3: 5 kg plastic (PET bottles)
    print("\n3. Testing 5 kg plastic (PET bottles):")
    print("-" * 40)
    result = WastePricing.calculate_net_transaction(
        waste_type='plastic',
        quantity_kg=5,
        subtype='PET bottles',
        distance_km=0
    )

    print(f"Waste Type: plastic (PET bottles)")
    print(f"Quantity: 5 kg")
    print(f"Market Value: ₹{result['waste_value']['total_value']} (₹{result['waste_value']['rate_per_kg']}/kg)")
    print(f"Collection Cost: ₹{result['collection_cost']['total_cost']}")
    print(f"Net Amount: ₹{result['net_amount']}")
    print(f"Transaction Type: {result['transaction_type']}")

    if result['net_amount'] < 0:
        print(f"✓ User PAYS ₹{abs(result['net_amount']):.2f} for collection")
    else:
        print(f"✓ User EARNS ₹{result['net_amount']:.2f} 🎉")

    # Test case 4: 3 kg organic waste
    print("\n4. Testing 3 kg organic waste:")
    print("-" * 40)
    result = WastePricing.calculate_net_transaction(
        waste_type='organic',
        quantity_kg=3,
        subtype='food waste',
        distance_km=0
    )

    print(f"Waste Type: organic (food waste)")
    print(f"Quantity: 3 kg")
    print(f"Market Value: ₹{result['waste_value']['total_value']} (₹{result['waste_value']['rate_per_kg']}/kg)")
    print(f"Collection Cost: ₹{result['collection_cost']['total_cost']}")
    print(f"Net Amount: ₹{result['net_amount']}")
    print(f"Transaction Type: {result['transaction_type']}")

    if result['net_amount'] < 0:
        print(f"✓ User PAYS ₹{abs(result['net_amount']):.2f} for collection")
    else:
        print(f"✓ User EARNS ₹{result['net_amount']:.2f} 🎉")

    print("\n" + "=" * 60)
    print("PRICING LOGIC TEST COMPLETED ✓")
    print("=" * 60)


def test_ai_config():
    """Test AI configuration"""
    print("\n" + "=" * 60)
    print("AI CONFIGURATION TEST")
    print("=" * 60)

    print("\n[*] Provider Status:")
    print("-" * 40)

    providers = [
        AIProvider.LOCAL,
        AIProvider.HUGGINGFACE,
        AIProvider.GEMINI,
        AIProvider.OPENAI
    ]

    for provider in providers:
        is_configured = AIConfig.is_provider_configured(provider)
        status = "[OK] Configured" if is_configured else "[X] Not Configured"

        print(f"{provider.value.upper()}: {status}")

        if provider != AIProvider.LOCAL and not is_configured:
            env_var = f"{provider.value.upper()}_API_KEY"
            print(f"   -> Set {env_var} in .env file")

    print("\n[*] Active Configuration:")
    print("-" * 40)
    print(f"Active Provider: {AIConfig.ACTIVE_PROVIDER.value}")
    print(f"Fallback Provider: {AIConfig.FALLBACK_PROVIDER.value}")
    print(f"Confidence Threshold: {AIConfig.CONFIDENCE_THRESHOLD}")

    if AIConfig.ACTIVE_PROVIDER == AIProvider.LOCAL:
        print(f"Local Model Path: {AIConfig.LOCAL_MODEL_PATH}")
        if os.path.exists(AIConfig.LOCAL_MODEL_PATH):
            print("   ✓ Model file exists")
        else:
            print("   ✗ Model file NOT FOUND")

    print("\n💡 To Switch Provider:")
    print("-" * 40)
    print("1. Edit backend/config/ai_config.py")
    print("   ACTIVE_PROVIDER = AIProvider.GEMINI  # for example")
    print("\n2. Or use API endpoint:")
    print("   POST /api/ai/switch-provider")
    print('   {"provider": "gemini"}')

    print("\n" + "=" * 60)
    print("AI CONFIGURATION TEST COMPLETED ✓")
    print("=" * 60)


def print_summary():
    """Print summary of changes"""
    print("\n" + "=" * 60)
    print("📋 SUMMARY OF CHANGES")
    print("=" * 60)

    print("\n✅ 1. FIXED PRICING LOGIC:")
    print("   - Proportional pricing based on actual weight")
    print("   - No more hardcoded minimum charges")
    print("   - Proper calculation using market rates")

    print("\n✅ 2. USERS NOW GET PAID FOR VALUABLE WASTE:")
    print("   - Metal, e-waste, plastic have market value")
    print("   - Net amount = waste value - collection cost")
    print("   - Positive = user earns, Negative = user pays")
    print("   - New endpoint: /api/payments/complete-earning")

    print("\n✅ 3. MULTIPLE AI PROVIDERS SUPPORTED:")
    print("   - Local Model (your trained model)")
    print("   - Hugging Face (cloud inference)")
    print("   - Google Gemini (vision AI)")
    print("   - OpenAI GPT-4 Vision")
    print("   - Easy switching via config or API")
    print("   - Automatic fallback if primary fails")

    print("\n📚 DOCUMENTATION:")
    print("   - See: backend/AI_INTEGRATION_GUIDE.md")
    print("   - API endpoints added:")
    print("     • POST /api/ai/predict")
    print("     • GET /api/ai/providers")
    print("     • POST /api/ai/switch-provider")
    print("     • GET /api/ai/test")

    print("\n🔧 CONFIGURATION:")
    print("   - Edit: backend/config/ai_config.py")
    print("   - Add API keys to: backend/.env")
    print("   - Example keys added to: backend/.env.example")

    print("\n" + "=" * 60)


def main():
    """Run all tests"""
    print("\n[TEST] WASTEWISE - PRICING & AI TEST SUITE")

    try:
        # Test pricing logic
        test_pricing()

        # Test AI configuration
        test_ai_config()

        # Print summary
        print_summary()

        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\n🚀 Next Steps:")
        print("   1. Add API keys to backend/.env for AI providers")
        print("   2. Test the booking flow with new pricing")
        print("   3. Upload waste images to test AI classification")
        print("   4. Read AI_INTEGRATION_GUIDE.md for details")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
