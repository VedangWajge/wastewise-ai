"""
Test script to verify FastAI provider integration
Run this to test the new FastAI provider
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from config.ai_config import AIConfig, AIProvider

def test_fastai_provider():
    """Test FastAI provider configuration and availability"""
    
    print("=" * 60)
    print("FastAI Provider Integration Test")
    print("=" * 60)
    
    # Check if FastAI is in the enum
    print("\n1. Checking AIProvider enum...")
    providers = [p.value for p in AIProvider]
    print(f"   Available providers: {providers}")
    assert 'fastai' in providers, "❌ FASTAI not found in AIProvider enum"
    print("   ✅ FASTAI found in enum")
    
    # Check if model file exists
    print("\n2. Checking FastAI model file...")
    model_path = AIConfig.FASTAI_MODEL_PATH
    print(f"   Model path: {model_path}")
    if os.path.exists(model_path):
        file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"   ✅ Model file exists ({file_size_mb:.2f} MB)")
    else:
        print(f"   ❌ Model file NOT found at {model_path}")
        return False
    
    # Check if provider is configured
    print("\n3. Checking provider configuration...")
    is_configured = AIConfig.is_provider_configured(AIProvider.FASTAI)
    print(f"   Is configured: {is_configured}")
    if is_configured:
        print("   ✅ FastAI provider is properly configured")
    else:
        print("   ❌ FastAI provider is NOT configured")
        return False
    
    # Get provider info
    print("\n4. Getting provider status...")
    provider_info = AIConfig.get_provider_info()
    print(f"   Active provider: {provider_info['active_provider']}")
    print(f"   Provider status:")
    for provider, status in provider_info['providers_status'].items():
        status_icon = "✅" if status else "❌"
        print(f"      {status_icon} {provider}: {status}")
    
    # Test switching to FastAI
    print("\n5. Testing provider switching...")
    original_provider = AIConfig.ACTIVE_PROVIDER
    print(f"   Original provider: {original_provider.value}")
    
    success = AIConfig.switch_provider(AIProvider.FASTAI)
    if success:
        print(f"   ✅ Successfully switched to FASTAI")
        print(f"   Current provider: {AIConfig.ACTIVE_PROVIDER.value}")
        
        # Switch back
        AIConfig.switch_provider(original_provider)
        print(f"   Switched back to: {AIConfig.ACTIVE_PROVIDER.value}")
    else:
        print(f"   ❌ Failed to switch to FASTAI")
        return False
    
    # Test FastAI provider import
    print("\n6. Testing FastAI provider import...")
    try:
        from providers.fastai_provider import FastAIProvider
        print("   ✅ FastAIProvider imported successfully")
        
        # Try to instantiate (this will load the model)
        print("\n7. Testing FastAI provider instantiation...")
        provider = FastAIProvider()
        print("   ✅ FastAI provider instantiated successfully")
        print(f"   Model vocab size: {len(provider.learner.dls.vocab)}")
        print(f"   Model classes: {list(provider.learner.dls.vocab)}")
        
    except ImportError as e:
        print(f"   ❌ Failed to import FastAIProvider: {e}")
        print(f"   Note: You may need to install fastai: pip install fastai")
        return False
    except Exception as e:
        print(f"   ❌ Failed to instantiate provider: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nTo use FastAI provider, set in ai_config.py:")
    print("   AIConfig.ACTIVE_PROVIDER = AIProvider.FASTAI")
    print("\nOr switch via API:")
    print("   POST /api/ai/switch-provider")
    print('   {"provider": "fastai"}')
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = test_fastai_provider()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
