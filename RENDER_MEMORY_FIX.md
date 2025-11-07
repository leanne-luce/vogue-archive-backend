# Render Memory Issue - Solutions

## Problem
CLIP model (~350MB) + dependencies exceed Render free tier's 512MB RAM limit.

## Solutions (Choose One)

### Option 1: Upgrade Render to Starter Plan ($7/month) ⭐ Recommended
**Pros:**
- 512MB → 2GB RAM (plenty for CLIP)
- No cold starts (always-on)
- Faster response times
- Simple - just upgrade the plan

**How:**
1. Go to Render dashboard
2. Select your `vogue-archive-api` service
3. Settings → Change Instance Type → "Starter" ($7/month)
4. Confirm

**Total cost: $7/month (still free Pinecone)**

### Option 2: Use Smaller Model (Free but Less Accurate)
Switch to a smaller model that fits in 512MB RAM but won't be as good for fashion.

**Changes needed:**
- Use `all-MiniLM-L6-v2` (80MB) instead of CLIP
- Re-process data with smaller model
- Lose multimodal search capability

### Option 3: Deploy to Different Platform
**Free alternatives with more memory:**
- **Railway**: Free tier with 512MB RAM (same issue)
- **Fly.io**: 256MB shared RAM (worse)
- **Google Cloud Run**: 512MB default (same issue)
- **AWS Lambda**: 512MB-10GB (complex setup)

**Better free option:**
- **Hugging Face Spaces**: 16GB RAM for free! But slower cold starts

### Option 4: Optimize Model Loading (Try First - Free!)
Reduce memory usage with optimizations:

**Changes in `api/app.py`:**
```python
import os
os.environ['TRANSFORMERS_CACHE'] = '/tmp'
os.environ['HF_HOME'] = '/tmp'
```

**Changes in `api/search.py`:**
```python
# Load with memory optimizations
self.model = SentenceTransformer(
    'clip-ViT-B-32',
    device='cpu',
    cache_folder='/tmp'
)
# Enable model quantization to reduce size
self.model.half()  # Use FP16 instead of FP32 (half the memory)
```

This might reduce memory to ~200-250MB. Worth trying!

## Recommended Path

1. **Try Option 4 first** (optimizations - free)
2. **If still failing → Option 1** (upgrade to Starter - $7/month)

Option 1 is the best long-term solution because:
- No cold starts = better UX
- Plenty of headroom for scaling to 10k+ items
- Can add more features later
- $7/month is reasonable for a production app

## Current Status

Your deployment is failing with OOM (Out of Memory) errors on Render free tier.

Choose one of the options above to proceed!
