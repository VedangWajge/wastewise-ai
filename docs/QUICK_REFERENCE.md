# WasteWise - Quick Reference Guide

## 🚀 Quick Start

### Switch AI Provider

**In Code (`backend/config/ai_config.py`):**
```python
ACTIVE_PROVIDER = AIProvider.GEMINI  # local, huggingface, gemini, openai
```

**Via API:**
```bash
curl -X POST http://localhost:5000/api/ai/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini"}'
```

### Add API Keys (`backend/.env`)
```bash
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

---

## 📊 Pricing Examples

### 2 kg Iron (Metal)
- Market Value: Rs. 40 (Rs. 20/kg)
- Collection Cost: Rs. 48.88
- **Result: User PAYS Rs. 8.88**

### 10 kg Copper (Metal)
- Market Value: Rs. 4,000 (Rs. 400/kg)
- Collection Cost: Rs. 124.64
- **Result: User EARNS Rs. 3,875.36** 🎉

### 5 kg PET Plastic
- Market Value: Rs. 75 (Rs. 15/kg)
- Collection Cost: Rs. 77.20
- **Result: User PAYS Rs. 2.20**

---

## 🤖 AI API Endpoints

### Classify Image
```bash
POST /api/ai/predict
curl -X POST http://localhost:5000/api/ai/predict \
  -F "image=@waste.jpg"
```

### Check Providers
```bash
GET /api/ai/providers
curl http://localhost:5000/api/ai/providers
```

### Switch Provider
```bash
POST /api/ai/switch-provider
curl -X POST http://localhost:5000/api/ai/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "local"}'
```

---

## 💰 Payment Endpoints

### For Valuable Waste (User Earns)
```bash
POST /api/payments/complete-earning
{
  "booking_id": "book_001"
}
```

### For Low-Value Waste (User Pays)
```bash
POST /api/payments/initiate
{
  "booking_id": "book_001",
  "amount": 50.00,
  "payment_method": "card"
}
```

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `backend/config/ai_config.py` | AI provider settings |
| `backend/.env` | API keys and secrets |
| `backend/utils/pricing.py` | Pricing logic |
| `backend/models/unified_classifier.py` | AI classifier |

---

## 📝 Market Rates (Rs./kg)

### Metals
- Copper: Rs. 400
- Brass: Rs. 250
- Aluminum: Rs. 80
- Steel: Rs. 25
- Iron: Rs. 20

### Plastics
- PET bottles: Rs. 15
- PP: Rs. 14
- HDPE: Rs. 12
- Mixed: Rs. 10

### Paper
- Office paper: Rs. 10
- Newspaper: Rs. 8
- Mixed: Rs. 7

### Others
- Organic: Rs. 0 (free composting)
- Glass: Rs. 1.5-2

---

## 🌐 AI Provider Comparison

| Provider | Free Tier | Cost | Accuracy | Speed |
|----------|-----------|------|----------|-------|
| Local | Unlimited | $0 | Good | Fast |
| Hugging Face | 30k/month | ~$0.50 | Good | Medium |
| Gemini | 1,500/day | ~$2 | Excellent | Fast |
| OpenAI | $5 credit | ~$10 | Best | Medium |

*Cost per 1000 images

---

## 🔗 Get API Keys

- **Hugging Face:** https://huggingface.co/settings/tokens
- **Google Gemini:** https://makersuite.google.com/app/apikey
- **OpenAI:** https://platform.openai.com/api-keys

---

## 📚 Documentation

- **Full AI Guide:** `backend/AI_INTEGRATION_GUIDE.md`
- **Complete Summary:** `IMPLEMENTATION_COMPLETE.md`
- **This File:** `QUICK_REFERENCE.md`

---

## ✅ Checklist

### Before Using AI Providers:
- [ ] Copy `.env.example` to `.env`
- [ ] Add API keys to `.env`
- [ ] Choose provider in `ai_config.py`
- [ ] Test with `/api/ai/providers`

### Before Testing Pricing:
- [ ] Check market rates in `pricing.py`
- [ ] Understand earning vs. payment logic
- [ ] Test with different waste types
- [ ] Verify calculations

---

## 🆘 Troubleshooting

**AI Model Not Found?**
→ Check `models/waste_classifier_model.h5` exists

**API Key Error?**
→ Add key to `.env` file

**Wrong Pricing?**
→ Check waste subtype matches market rates

**Provider Not Working?**
→ Check `/api/ai/providers` for status

---

**Last Updated:** January 2025
**Version:** 1.0
