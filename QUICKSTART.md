# Vogue Archive Search - Quick Start

Everything is configured and ready to go! Follow these steps to get your search running.

## Your Setup

✅ **Pinecone API Key**: Configured in the Colab notebook
✅ **Pinecone Host**: `https://vogue-archive-5kcnmfq.svc.aped-4627-b74a.pinecone.io`
✅ **Index Name**: `vogue-archive`
✅ **Data Source**: Internet Archive Vogue Runway dataset (1.2M images)

---

## Step 1: Process Data in Google Colab (15 minutes)

The Colab notebook automatically downloads and processes the Vogue Runway dataset!

1. **Open the notebook**: [data-processing/process_vogue_data.ipynb](data-processing/process_vogue_data.ipynb)
2. **Upload to Google Colab**:
   - Go to https://colab.research.google.com/
   - File → Upload notebook
   - Select `process_vogue_data.ipynb`
3. **Run all cells**: Runtime → Run all
4. **What happens**:
   - Downloads Vogue Runway metadata (~300MB)
   - Extracts top 1000 fashion items by aesthetic quality
   - Generates semantic embeddings
   - Uploads to your Pinecone index
5. **Wait**: ~15-20 minutes total

### Sample Data You'll Get

```
Chanel Spring 2022 Ready-to-Wear from Paris Fashion Week
Valentino Fall 2021 Couture from Paris Fashion Week
Dior Resort 2023 Ready-to-Wear from Paris Fashion Week
```

Each with designer, season, year, category, city, and image URL!

---

## Step 2: Deploy API to Render (10 minutes)

### 2.1 Push to GitHub

```bash
cd vogue-archive-backend
git init
git add .
git commit -m "Add Vogue Archive Search API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/vogue-archive-backend.git
git push -u origin main
```

### 2.2 Deploy on Render

1. Go to https://render.com/ and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `vogue-archive-api`
   - **Root Directory**: `api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

5. Add **Environment Variables** (click "Advanced"):

   | Key | Value |
   |-----|-------|
   | `PINECONE_API_KEY` | `pcsk_2JKS4Y_LNuT72kmgxsuWksy2LyqcQP5Q2iX626vPCwb2KEjj23Vf72a43ZWgNp6FcCJshz` |
   | `PINECONE_INDEX_NAME` | `vogue-archive` |
   | `PINECONE_ENVIRONMENT` | `us-east-1-aws` |

6. Click **"Create Web Service"**
7. Wait ~5-10 minutes for deployment
8. Copy your URL: `https://vogue-archive-api.onrender.com`

### 2.3 Test Your API

```bash
# Health check
curl https://vogue-archive-api.onrender.com/

# Test search
curl -X POST https://vogue-archive-api.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "elegant evening gowns", "top_k": 5}'
```

---

## Step 3: Update React Native App (1 minute)

1. Open `app/vogue-archive-search.tsx`
2. Line 10, replace:
   ```typescript
   const API_URL = 'https://your-app.onrender.com';
   ```
   With your actual Render URL:
   ```typescript
   const API_URL = 'https://vogue-archive-api.onrender.com';
   ```
3. Save the file

---

## Step 4: Test in Your App!

1. Open your React Native app
2. Navigate to "Vogue Archive Search"
3. Try searching:
   - "Chanel tweed jacket"
   - "minimalist black dress"
   - "colorful summer collection"
   - "vintage cocktail dress"
   - "oversized blazer"

You should see results with:
- Designer name
- Season & year
- City (Paris, Milan, New York)
- Category (Ready-to-Wear, Couture, etc.)
- Match score

---

## What You Can Search

The semantic search understands fashion concepts:

**Style Queries**:
- "elegant evening gowns"
- "casual streetwear"
- "minimalist aesthetic"
- "vintage inspired"

**Item Queries**:
- "red dress"
- "leather jacket"
- "floral print"
- "tailored blazer"

**Designer Queries**:
- "Chanel classic"
- "Dior evening wear"
- "Valentino couture"

**Era Queries**:
- "90s grunge"
- "modern minimalism"
- "Art Deco inspired"

---

## Advanced: Filters

You can add filters to your searches in the API:

```typescript
const response = await fetch(`${API_URL}/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'elegant dresses',
    top_k: 10,
    filters: {
      designer: 'Chanel',
      season: 'Spring',
      year: 2022,
      city: 'Paris',
      min_aesthetic: 7.0  // Only high-quality images
    }
  })
});
```

Available filters:
- `designer`: Exact designer name
- `season`: Spring, Fall, Resort, Pre-Fall
- `year`: Specific year
- `year_range`: `{min: 2020, max: 2023}`
- `category`: Ready-to-Wear, Couture, etc.
- `city`: Paris, Milan, New York, London
- `min_aesthetic`: Minimum quality score (0-10)

---

## Scaling Up

### Current Setup (Free)
- **1,000 fashion items** in Pinecone
- **Free tier** on both Pinecone and Render
- **Search speed**: ~100-200ms
- **Cost**: $0/month

### To Add More Data

Want 10k or 100k items? Edit the Colab notebook:

```python
# Change this line in Cell 8:
df = df.nlargest(1000, 'aesthetic')  # Change 1000 to 10000

# Or process ALL 1.2M items:
# df = df  # Use entire dataset (requires Pinecone upgrade)
```

Then re-run the notebook.

### Production Setup
- **100,000 items**: Free tier still works!
- **1,000,000+ items**: Upgrade to Pinecone Standard ($70/month)
- **No cold starts**: Upgrade Render to Starter ($7/month)

---

## Troubleshooting

### "Index not found" error
- Make sure you created the Pinecone index named `vogue-archive`
- Check the index exists at https://app.pinecone.io/

### "No results found"
- Make sure you ran the Colab notebook to populate data
- Check index stats: `curl https://your-api.onrender.com/stats`

### API slow first request
- **Normal!** Free tier has ~30 second cold start
- Subsequent requests are fast (~200ms)

### Build failed on Render
- Check "Root Directory" is set to `api`
- Check environment variables are correct

---

## Next Steps

1. ✅ Run Colab notebook
2. ✅ Deploy to Render
3. ✅ Update app with API URL
4. ✅ Test search functionality
5. 🎨 Optional: Add filter UI in the app
6. 🎨 Optional: Display runway images
7. 🎨 Optional: Process more items (10k, 100k)

---

## Documentation

- **Data Source Guide**: [data-processing/VOGUE_RUNWAY_GUIDE.md](data-processing/VOGUE_RUNWAY_GUIDE.md)
- **Full Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Documentation**: [docs/API.md](docs/API.md)
- **Setup Instructions**: [docs/SETUP.md](docs/SETUP.md)

---

## Questions?

Everything is configured with your API key and ready to run. Just follow the 3 steps above and you'll have semantic fashion search working in ~30 minutes total!
