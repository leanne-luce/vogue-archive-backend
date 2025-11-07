# Setup Guide

## Step 1: Process Data (Google Colab)

### 1.1 Get Pinecone API Key
1. Sign up at https://www.pinecone.io/ (free tier)
2. Create a new project
3. Copy your API key from the dashboard

### 1.2 Run Data Processing
1. Open `data-processing/process_vogue_data.ipynb` in Google Colab
2. Click "Runtime" → "Change runtime type" → Select "GPU"
3. In the notebook, replace `your-api-key-here` with your Pinecone API key
4. Run all cells (Cmd+Enter on each cell)
5. Wait ~20 minutes for processing to complete

### 1.3 Verify Data Upload
The notebook will print:
```
Upload complete! 10000 vectors in Pinecone.
```

## Step 2: Deploy API (Render.com)

### 2.1 Push to GitHub
```bash
cd vogue-archive-backend
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/vogue-archive-backend.git
git push -u origin main
```

### 2.2 Deploy to Render
1. Sign up at https://render.com (free tier)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: vogue-archive-api
   - **Root Directory**: `api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 2.3 Add Environment Variables
In Render dashboard, go to "Environment" tab and add:
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_INDEX_NAME`: `vogue-archive`
- `PINECONE_ENVIRONMENT`: `us-east-1-aws`

### 2.4 Deploy
Click "Create Web Service" and wait 5-10 minutes for deployment.

Your API URL will be: `https://vogue-archive-api.onrender.com`

### 2.5 Test the API
```bash
curl -X POST https://vogue-archive-api.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "elegant evening gowns", "top_k": 5}'
```

## Step 3: Connect React Native App

See the main README for integration steps.

## Troubleshooting

### Cold Starts
- Render free tier has cold starts (~30 seconds)
- First request after 15 minutes of inactivity will be slow

### API Errors
- Check Render logs in dashboard
- Verify environment variables are set
- Ensure Pinecone index has data

### Pinecone Quota
- Free tier: 1 index, 100k vectors
- If you need more, upgrade to paid tier ($70/month for 10M vectors)
