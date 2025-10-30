# AI Waste Classification Integration Guide

## Overview

WasteWise now supports **multiple AI providers** for waste classification with easy switching between them:

1. **Local Model** - Your trained TensorFlow/Keras model
2. **Hugging Face** - Cloud-based inference API
3. **Google Gemini** - Google's vision AI (Gemini 1.5)
4. **OpenAI** - GPT-4 Vision API

## Quick Setup

### 1. Choose Your AI Provider

Edit `backend/config/ai_config.py` and set:

```python
ACTIVE_PROVIDER = AIProvider.LOCAL  # or HUGGINGFACE, GEMINI, OPENAI
```

Or set in `.env` file:
```bash
AI_PROVIDER=local  # or huggingface, gemini, openai
```

### 2. Configure API Keys

Add your API keys to `backend/.env`:

```bash
# Hugging Face
HUGGINGFACE_API_KEY=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Google Gemini
GEMINI_API_KEY=AIzaSyAbSgdrh57BYh29axShDJTSIbOwo2ij5b4

# OpenAI
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 3. Install Dependencies

```bash
# For Hugging Face
pip install requests

# For Google Gemini
pip install google-generativeai

# For OpenAI (already using requests)
# No additional packages needed
```

## API Endpoints

### 1. Classify Waste Image

**POST** `/api/ai/predict`

Upload an image to classify waste type.

**Request:**
```bash
curl -X POST http://localhost:5000/api/ai/predict \
  -F "image=@waste_photo.jpg"
```

**Response:**
```json
{
  "success": true,
  "waste_type": "plastic",
  "raw_category": "plastic",
  "confidence": 0.95,
  "provider_used": "local",
  "fallback_used": false,
  "recommendations": [
    "Check recycling number on the bottom",
    "Rinse containers before recycling",
    "Remove caps (often different plastic type)"
  ],
  "all_predictions": [
    {"class": "plastic", "confidence": 0.95},
    {"class": "metal", "confidence": 0.03}
  ],
  "timestamp": "2025-01-15T10:30:00"
}
```

### 2. Get Provider Information

**GET** `/api/ai/providers`

Get status of all AI providers.

**Response:**
```json
{
  "success": true,
  "provider_info": {
    "active_provider": "local",
    "fallback_provider": "huggingface",
    "providers_status": {
      "local": true,
      "huggingface": true,
      "gemini": false,
      "openai": false
    }
  }
}
```

### 3. Switch AI Provider

**POST** `/api/ai/switch-provider`

Switch to a different AI provider at runtime.

**Request:**
```bash
curl -X POST http://localhost:5000/api/ai/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Switched to gemini provider",
  "active_provider": "gemini"
}
```

### 4. Test AI Service

**GET** `/api/ai/test`

Check if AI service is working.

**Response:**
```json
{
  "success": true,
  "message": "AI service is running",
  "active_provider": "local",
  "provider_status": { ... }
}
```

## Provider Details

### Local Model (Default)

- **Pros**: Fast, free, offline, privacy-preserving
- **Cons**: Requires model file, limited accuracy
- **Setup**: Ensure `models/waste_classifier_model.h5` exists

```python
# In config/ai_config.py
ACTIVE_PROVIDER = AIProvider.LOCAL
LOCAL_MODEL_PATH = 'models/waste_classifier_model.h5'
```

### Hugging Face

- **Pros**: Good accuracy, reasonable cost, many models available
- **Cons**: Requires internet, API key
- **Cost**: Free tier: 30,000 requests/month
- **Setup**: Get API key from https://huggingface.co/settings/tokens

```python
ACTIVE_PROVIDER = AIProvider.HUGGINGFACE
HUGGINGFACE_MODEL = 'timm/efficientnet_b0.ra_in1k'
```

Alternative models you can try:
- `microsoft/resnet-50`
- `google/vit-base-patch16-224`
- `facebook/deit-base-patch16-224`

### Google Gemini

- **Pros**: Excellent accuracy, multimodal, fast
- **Cons**: Requires API key, usage costs
- **Cost**: Free tier: 60 requests/minute
- **Setup**: Get API key from https://makersuite.google.com/app/apikey

```python
ACTIVE_PROVIDER = AIProvider.GEMINI
GEMINI_MODEL = 'gemini-1.5-flash'  # or 'gemini-pro-vision'
```

### OpenAI GPT-4 Vision

- **Pros**: Best accuracy, detailed reasoning
- **Cons**: Most expensive, requires API key
- **Cost**: ~$0.01 per image
- **Setup**: Get API key from https://platform.openai.com/api-keys

```python
ACTIVE_PROVIDER = AIProvider.OPENAI
OPENAI_MODEL = 'gpt-4o'  # or 'gpt-4-vision-preview'
```

## Pricing Comparison

| Provider | Cost per 1000 images | Free Tier | Speed |
|----------|---------------------|-----------|-------|
| Local | $0 | Unlimited | Fast |
| Hugging Face | ~$0.50 | 30k/month | Medium |
| Gemini | ~$2 | 1,500/day | Fast |
| OpenAI | ~$10 | $5 credit | Medium |

## Fallback Strategy

The system automatically falls back to the secondary provider if the primary fails:

```python
# In config/ai_config.py
ACTIVE_PROVIDER = AIProvider.GEMINI
FALLBACK_PROVIDER = AIProvider.LOCAL
```

If Gemini fails (API error, rate limit, etc.), it automatically uses the local model.

## Testing Different Providers

### Python Script

```python
from models.unified_classifier import UnifiedWasteClassifier
from config.ai_config import AIProvider

# Test with different providers
providers = [AIProvider.LOCAL, AIProvider.GEMINI, AIProvider.OPENAI]

for provider in providers:
    classifier = UnifiedWasteClassifier(provider)
    result = classifier.classify('test_image.jpg')
    print(f"{provider.value}: {result['waste_type']} ({result['confidence']:.2%})")
```

### Using API

```bash
# Test local model
curl -X POST http://localhost:5000/api/ai/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "local"}'

curl -X POST http://localhost:5000/api/ai/predict \
  -F "image=@test.jpg"

# Test Gemini
curl -X POST http://localhost:5000/api/ai/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini"}'

curl -X POST http://localhost:5000/api/ai/predict \
  -F "image=@test.jpg"
```

## Troubleshooting

### Local Model Not Found

```
[ERROR] Failed to load model: ...
```

**Solution**: Ensure `models/waste_classifier_model.h5` exists or train a new model.

### API Key Errors

```
ValueError: GEMINI_API_KEY not configured
```

**Solution**: Add API key to `.env` file:
```bash
GEMINI_API_KEY=your_actual_key_here
```

### Rate Limit Errors

```
RuntimeError: Hugging Face API error: Rate limit exceeded
```

**Solution**:
1. Wait a few minutes
2. Switch to fallback provider
3. Upgrade to paid tier

### Low Confidence Results

```json
{"confidence": 0.45}
```

**Solution**:
1. Use a better quality image
2. Try a different AI provider
3. Adjust `CONFIDENCE_THRESHOLD` in config

## Advanced Configuration

### Custom Waste Categories

Edit `config/ai_config.py`:

```python
WASTE_CATEGORIES = [
    'battery', 'biological', 'cardboard',
    'your_custom_category',  # Add your own
    # ...
]

CATEGORY_MAPPING = {
    'your_custom_category': 'custom',  # Map to app types
    # ...
}
```

### Adjust Confidence Threshold

```python
CONFIDENCE_THRESHOLD = 0.7  # Only accept results >= 70%
```

### Change Hugging Face Model

```python
HUGGINGFACE_MODEL = 'microsoft/resnet-50'  # Try different model
```

## Best Practices

1. **Start with Local Model** for development/testing
2. **Use Gemini** for production (good balance of cost/accuracy)
3. **Set up Fallback** to Local model for reliability
4. **Monitor API Usage** to avoid unexpected costs
5. **Cache Results** for frequently classified items
6. **Log Provider Performance** to optimize selection

## Cost Optimization

### For Development
```python
ACTIVE_PROVIDER = AIProvider.LOCAL
FALLBACK_PROVIDER = AIProvider.HUGGINGFACE
```

### For Production (Low Budget)
```python
ACTIVE_PROVIDER = AIProvider.LOCAL
FALLBACK_PROVIDER = AIProvider.GEMINI
```

### For Production (High Accuracy)
```python
ACTIVE_PROVIDER = AIProvider.GEMINI
FALLBACK_PROVIDER = AIProvider.LOCAL
```

## Integration with Booking System

The AI classification now integrates with the updated pricing system:

1. **User uploads waste image** → AI classifies waste type
2. **System calculates value** using `utils/pricing.py`
3. **User sees earnings or cost**:
   - **Valuable waste** (metal, e-waste): User gets PAID
   - **Low-value waste** (organic): User pays for collection

Example for 2kg iron:
- Market value: ₹20/kg × 2kg = ₹40
- Collection cost: ₹30 base + (₹8/kg × 2kg) × 1.18 = ₹54.48
- **Net: User pays ₹14.48** (collection cost exceeds value)

Example for 10kg copper:
- Market value: ₹400/kg × 10kg = ₹4,000
- Collection cost: ₹30 + (₹8/kg × 10kg) × 1.18 = ₹124.64
- **Net: User earns ₹3,875.36** 🎉

## Support

For issues or questions:
1. Check provider status: `/api/ai/providers`
2. Test endpoint: `/api/ai/test`
3. Review logs in `app.log`
4. Check API key validity

## Future Enhancements

- [ ] Add Azure Computer Vision support
- [ ] Implement result caching
- [ ] Add batch classification
- [ ] Create mobile SDKs
- [ ] Add A/B testing for providers
- [ ] Implement cost tracking dashboard
