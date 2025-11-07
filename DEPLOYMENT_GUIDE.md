# Vogue Archive Search - Deployment Guide

## Your Configuration

**Pinecone API Key**: `pcsk_2JKS4Y_LNuT72kmgxsuWksy2LyqcQP5Q2iX626vPCwb2KEjj23Vf72a43ZWgNp6FcCJshz`
**Index Name**: `vogue-archive`
**Region**: `us-east-1`

---

## Step 1: Create Pinecone Index (5 minutes)

1. Go to https://app.pinecone.io/
2. Log in with your account
3. Click **"Create Index"**
4. Fill in the details:
   - **Name**: `vogue-archive`
   - **Dimensions**: `384`
   - **Metric**: `cosine`
   - **Region**: `us-east-1`
   - **Plan**: Starter (free)
5. Click **Create Index**

**Note**: The index will be empty at first. You'll populate it in Step 2.

---

## Step 2: Process Data in Google Colab (20 minutes)

### Before you start:
You need Vogue archive data in this format:
```json
[
  {
    "id": "vogue_1950_01_p15",
    "year": 1950,
    "month": 1,
    "page": 15,
    "description": "Christian Dior New Look: Full skirted silhouette",
    "image_url": "https://...",
    "designer": "Christian Dior",
    "category": "Evening Wear"
  }
]
```

### Steps:
1. Open [Google Colab](https://colab.research.google.com/)
2. Upload `data-processing/process_vogue_data.ipynb`
3. Your API key is already configured in the notebook
4. Replace the sample data in Cell 8 with your actual Vogue data
5. Click **Runtime → Run all**
6. Wait ~20 minutes while it processes

### What happens:
- Installs Python packages
- Connects to your Pinecone index
- Generates embeddings for each fashion item
- Uploads vectors to Pinecone
- Tests search functionality

---

## Step 3: Deploy API to Render (10 minutes)

### 3.1 Push to GitHub

```bash
cd vogue-archive-backend
git init
git add .
git commit -m "Initial commit: Vogue Archive Search API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/vogue-archive-backend.git
git push -u origin main
```

### 3.2 Deploy on Render

1. Go to https://render.com/
2. Sign up / Log in
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub account
5. Select your `vogue-archive-backend` repository
6. Configure the service:
   - **Name**: `vogue-archive-api` (or anything you like)
   - **Region**: `Oregon (US West)` (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: `api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

7. Add **Environment Variables**:
   - Click **"Advanced"**
   - Add these variables:

   | Key | Value |
   |-----|-------|
   | `PINECONE_API_KEY` | `pcsk_2JKS4Y_LNuT72kmgxsuWksy2LyqcQP5Q2iX626vPCwb2KEjj23Vf72a43ZWgNp6FcCJshz` |
   | `PINECONE_INDEX_NAME` | `vogue-archive` |
   | `PINECONE_ENVIRONMENT` | `us-east-1-aws` |

8. Click **"Create Web Service"**
9. Wait ~5 minutes for deployment
10. Your API will be live at: `https://vogue-archive-api.onrender.com`

### 3.3 Test Your API

```bash
curl https://vogue-archive-api.onrender.com/

# Should return: {"status": "ok", "message": "Vogue Archive Search API"}
```

Test search:
```bash
curl -X POST https://vogue-archive-api.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "elegant evening gowns", "top_k": 5}'
```

---

## Step 4: Update React Native App (2 minutes)

1. Open `app/vogue-archive-search.tsx`
2. Find line 10:
   ```typescript
   const API_URL = 'https://your-app.onrender.com';
   ```
3. Replace with your actual Render URL:
   ```typescript
   const API_URL = 'https://vogue-archive-api.onrender.com';
   ```
4. Save the file
5. Test the search feature in your app!

---

## Troubleshooting

### Render Deployment Issues

**Problem**: "Build failed"
- **Solution**: Make sure you set **Root Directory** to `api`

**Problem**: "Application failed to respond"
- **Solution**: Check environment variables are set correctly

### Cold Starts
On the free tier, your API "sleeps" after 15 minutes of inactivity.
- **First request**: ~30 seconds (cold start)
- **Subsequent requests**: ~200ms

To avoid this, upgrade to paid tier ($7/month) for always-on service.

### Pinecone Issues

**Problem**: "Index not found"
- **Solution**: Make sure you created the index with name `vogue-archive`

**Problem**: "Invalid API key"
- **Solution**: Double-check the API key in environment variables

### No Search Results

**Problem**: API works but returns empty results
- **Solution**: Make sure you ran the Colab notebook to populate data

---

## Next Steps

Once deployed:
1. Test search in your React Native app
2. Gather Vogue archive data (images + descriptions)
3. Re-run Colab notebook with real data
4. Optionally: Add filters (year, designer, category)
5. Optionally: Add image search capabilities

---

## Cost Summary

- **Pinecone Starter**: Free (100k vectors, 1 index)
- **Render Free Tier**: Free (750 hours/month, cold starts)
- **Google Colab**: Free (with usage limits)

**Total: $0/month**

For production:
- **Pinecone Standard**: $70/month (1M vectors)
- **Render Starter**: $7/month (no cold starts)

**Total: $77/month**
