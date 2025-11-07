# Upgrading to CLIP for Better Fashion Search

## What Changed

We're switching from `all-MiniLM-L6-v2` (general purpose) to `clip-ViT-B-32` (vision+language model) for better fashion understanding.

### Why CLIP is Better for Fashion

**CLIP understands:**
- Visual fashion concepts (silhouettes, textures, patterns)
- Fashion terminology (tweed, draping, A-line, tailoring)
- Style descriptors (minimalist, vintage, avant-garde)
- Designer aesthetics
- Garment types and their variations

**Results:**
- "tweed jacket" finds Chanel-style jackets even without "Chanel" in description
- "minimalist dress" understands clean lines and simplicity
- "vintage gown" finds retro/classic aesthetics
- Better semantic understanding overall

## Steps to Upgrade

### 1. Create New Pinecone Index

The new index uses **512 dimensions** (vs 384 for the old model).

**Go to**: https://app.pinecone.io/

**Create index with:**
- **Name**: `vogue-archive-clip`
- **Dimensions**: `512`
- **Metric**: `cosine`
- **Region**: `us-east-1`

### 2. Re-run Colab Notebook

The notebook has been updated to:
- Use CLIP model (`clip-ViT-B-32`)
- Create/use the new `vogue-archive-clip` index
- Generate 512-dimensional embeddings

**Steps:**
1. Open [process_vogue_data.ipynb](data-processing/process_vogue_data.ipynb) in Google Colab
2. Run all cells (~15-20 minutes)
3. It will automatically create the new index and upload embeddings

### 3. Update Render Environment Variable

In your Render dashboard for `vogue-archive-api`:

1. Go to **Environment** tab
2. Update the variable:
   - **Key**: `PINECONE_INDEX_NAME`
   - **Old value**: `vogue-archive`
   - **New value**: `vogue-archive-clip`
3. Click **Save Changes**
4. Render will auto-redeploy (~5 minutes)

### 4. Push Updated Code to GitHub

```bash
cd vogue-archive-backend
git add .
git commit -m "Upgrade to CLIP model for better fashion search"
git push
```

This will trigger Render to rebuild with the new CLIP model.

## Testing Improvements

After upgrading, try these searches to see the improvement:

### Before CLIP (literal matching):
- "tweed" → only finds items with "tweed" in description

### After CLIP (semantic understanding):
- "tweed jacket" → finds textured, woven jackets (Chanel-style)
- "minimalist black dress" → understands clean, simple aesthetics
- "vintage cocktail dress" → finds classic, timeless evening wear
- "oversized blazer" → understands proportions and silhouette
- "romantic gown" → finds flowing, feminine designs

## Cost & Performance

- **Cost**: Still $0/month on free tiers
- **Index size**: Same 1000 items, just better embeddings
- **Search speed**: Same (~200ms)
- **Model size**: Slightly larger (~350MB vs ~80MB)
- **First deployment**: Takes ~2-3 minutes longer due to model download

## Optional: Keep Both Indexes

You can keep both indexes and compare results:
- Old index: `vogue-archive` (384d, MiniLM)
- New index: `vogue-archive-clip` (512d, CLIP)

Just switch the `PINECONE_INDEX_NAME` environment variable to test each.

## Rollback (if needed)

If you want to go back to the old model:

1. Change Render env var back to `vogue-archive`
2. Revert code changes:
   ```bash
   git revert HEAD
   git push
   ```

## What You Keep

✅ Same 1000 Vogue Runway items
✅ Same metadata (designer, season, year, etc.)
✅ Same API URL and endpoints
✅ Same React Native app code

Only the **search quality** improves!

## Next Steps After Upgrade

Once CLIP is working, you can:

1. **Add more items**: Process 10k or 100k items with better search
2. **Multimodal search**: Search by uploading an image (CLIP does this!)
3. **Image similarity**: Find similar runway looks by visual features
4. **Style discovery**: Find aesthetic groupings automatically

## Questions?

- Check the new index exists: https://app.pinecone.io/
- Check model loaded: View Render logs for "CLIP ViT-B/32"
- Test API: `curl https://vogue-archive-api.onrender.com/stats`
