# Vogue Archive Search Backend

A semantic search API for exploring Vogue magazine archives using vector embeddings and Pinecone.

## Architecture

```
┌─────────────────────────────────────────┐
│ 1. PROCESS DATA (One-time)             │
│    Run on: Google Colab (free GPU)     │
│    Time: 20 minutes                     │
│    Output: 10k vectors in Pinecone     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 2. DEPLOY API (Your backend)           │
│    Run on: Render.com (free tier)      │
│    Time: 5 minutes                      │
│    Output: https://your-api.com         │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 3. BUILD YOUR APPS                      │
│    React Native → Call API              │
│    iOS → Call API                       │
│    Your laptop / Xcode                  │
└─────────────────────────────────────────┘
```

## Project Structure

```
vogue-archive-backend/
├── README.md                 # This file
├── data-processing/          # Step 1: Colab notebooks & scripts
│   ├── process_vogue_data.ipynb
│   ├── requirements-colab.txt
│   └── sample_data.json
├── api/                      # Step 2: Render API backend
│   ├── app.py               # Flask/FastAPI server
│   ├── requirements.txt
│   ├── search.py            # Search logic
│   └── render.yaml          # Render deployment config
└── docs/
    ├── SETUP.md             # Setup instructions
    └── API.md               # API documentation
```

## Quick Start

### Prerequisites
- Pinecone account (free tier: https://www.pinecone.io/) ✅ **You have your API key**
- Render account (free tier: https://render.com/)
- Google Colab (free: https://colab.research.google.com/)

### Step 1: Process Data (Google Colab)
1. First, create your Pinecone index:
   - Go to https://app.pinecone.io/
   - Click "Create Index"
   - Name: `vogue-archive`
   - Dimension: `384` (for all-MiniLM-L6-v2 model)
   - Metric: `cosine`
   - Region: `us-east-1`

2. Open `data-processing/process_vogue_data.ipynb` in Google Colab
3. Add your Pinecone API key: `pcsk_2JKS4Y_LNuT72kmgxsuWksy2LyqcQP5Q2iX626vPCwb2KEjj23Vf72a43ZWgNp6FcCJshz`
4. Add your Vogue data (images + descriptions)
5. Run all cells (~20 minutes)
6. This creates embeddings and uploads to Pinecone

### Step 2: Deploy API (Render)
1. Push this repo to GitHub
2. Connect to Render.com
3. Deploy from `api/` directory
4. Add environment variables (Pinecone API key)
5. Get your API URL: `https://your-app.onrender.com`

### Step 3: Connect to React Native App
Update the Vogue Archive Search page to call your API:
```typescript
const response = await fetch('https://your-api.onrender.com/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'vintage Dior dresses' })
});
```

## Environment Variables

### For Colab (Step 1)
```
PINECONE_API_KEY=your-key-here
PINECONE_INDEX_NAME=vogue-archive
```

### For Render (Step 2)
```
PINECONE_API_KEY=your-key-here
PINECONE_INDEX_NAME=vogue-archive
PINECONE_ENVIRONMENT=us-east-1-aws
```

## API Endpoints

### POST /search
Search the Vogue archive with a text query.

**Request:**
```json
{
  "query": "elegant evening gowns from the 1950s",
  "top_k": 10
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "vogue_1955_03_p42",
      "score": 0.89,
      "metadata": {
        "year": 1955,
        "month": 3,
        "page": 42,
        "description": "Christian Dior evening gown...",
        "image_url": "https://..."
      }
    }
  ]
}
```

## Tech Stack

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: Pinecone (free tier: 1 index, 100k vectors)
- **API**: Flask (lightweight, easy to deploy)
- **Hosting**: Render.com (free tier with cold starts)

## Cost Breakdown

- **Pinecone Free Tier**: 1 index, up to 100k vectors (free forever)
- **Render Free Tier**: 750 hours/month (free forever, but cold starts)
- **Google Colab**: Free GPU access (limited runtime)

**Total Cost: $0/month**

## Next Steps

1. Get your Vogue archive data (images + text descriptions)
2. Run the Colab notebook to create embeddings
3. Deploy the API to Render
4. Connect your React Native app

## Notes

- Cold starts on Render free tier: ~30 seconds for first request
- Data processing needs to run once; updates can be incremental
- Consider upgrading to paid tiers for production use
