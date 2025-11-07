# Vogue Runway Dataset Guide

## Dataset Overview

**Source**: https://archive.org/details/VogueRunway_dataset
**Size**: 1,281,633 fashion runway images (854GB total)
**Format**: WebDataset .tar archives + Parquet metadata
**License**: Check Internet Archive for usage terms

## What's Included

The dataset contains runway images from Vogue with metadata:
- **Designer**: e.g., "Chanel", "Dior", "Prada"
- **Season**: e.g., "Spring", "Fall", "Resort"
- **Year**: e.g., 2020, 2021, 2022
- **Category**: e.g., "Ready-to-Wear", "Couture"
- **City**: e.g., "Paris", "Milan", "New York"
- **Section**: e.g., "Look 1", "Look 2"
- **Aesthetic Score**: Quality rating (0-10)
- **Image URL**: Link to the runway image

## Quick Start Options

### Option 1: Use Colab Directly (Easiest) ⭐

The Colab notebook now automatically downloads and processes the data!

1. Open [process_vogue_data.ipynb](process_vogue_data.ipynb) in Google Colab
2. Run all cells - it will:
   - Download the parquet metadata file (~300MB)
   - Extract top 1000 items by aesthetic score
   - Generate embeddings
   - Upload to your Pinecone index
3. **Runtime**: ~15-20 minutes total

**Pros**: No local setup needed, runs entirely in the cloud
**Cons**: Limited to 1000 items on free Colab (you can increase this)

### Option 2: Download Locally First

If you want more control or to process more items:

1. Install requirements:
   ```bash
   cd vogue-archive-backend/data-processing
   pip install -r requirements.txt
   ```

2. Run the download script:
   ```bash
   python download_vogue_data.py
   ```
   This will:
   - Download the metadata parquet (~300MB)
   - Select top 1000 items (configurable)
   - Save to `vogue_data/vogue_runway_prepared.json`

3. Upload the JSON file to Colab and process it there

**Pros**: More control over filtering, can process more items
**Cons**: Requires local Python setup

## Data Structure

The notebook prepares items in this format:

```json
{
  "id": "vogue_runway_0000123",
  "description": "Chanel Spring 2022 Ready-to-Wear from Paris Fashion Week",
  "metadata": {
    "designer": "Chanel",
    "season": "Spring",
    "year": 2022,
    "category": "Ready-to-Wear",
    "city": "Paris",
    "section": "Look 42",
    "image_url": "https://...",
    "aesthetic_score": 8.5
  }
}
```

This description is used to generate semantic embeddings for search.

## Filtering Options

You can customize what items to include by modifying the notebook:

### By Designer
```python
# Only include specific designers
designers = ['Chanel', 'Dior', 'Valentino']
df = df[df['designer'].isin(designers)]
```

### By Year Range
```python
# Only recent collections
df = df[df['year'] >= 2020]
```

### By Aesthetic Score
```python
# High quality images only
df = df[df['aesthetic'] >= 7.0]
```

### By Category
```python
# Only haute couture
df = df[df['category'] == 'Couture']
```

## Processing Full Dataset

The full dataset is **854GB** across 129 tar files. To process everything:

1. **Download all tar files** (requires ~1TB storage):
   ```bash
   wget -r -np -nd https://archive.org/download/VogueRunway_dataset/vogue_runway_*.tar
   ```

2. **Extract images** from tar files:
   ```python
   import tarfile
   # Extract tar files as needed
   ```

3. **Process in batches** (modify the notebook to loop through all items)

4. **Upgrade Pinecone** to handle more vectors:
   - Free tier: 100k vectors
   - Standard tier: 1M+ vectors ($70/month)

## Search Examples

Once uploaded to Pinecone, you can search like:

- "elegant evening gowns"
- "Chanel tweed jacket"
- "minimalist black dress"
- "colorful summer collection"
- "vintage-inspired cocktail dress"
- "oversized blazer streetwear"

The semantic search understands concepts, not just keywords!

## Next Steps

1. ✅ Run the Colab notebook to process 1000 items
2. ✅ Deploy the API to Render
3. ✅ Test search in your React Native app
4. Optional: Process more items (10k, 100k, or all 1.2M)
5. Optional: Add image search using CLIP embeddings (dataset includes these!)

## Performance Notes

- **1,000 items**: Loads in ~2 seconds, searches in ~100ms
- **10,000 items**: Loads in ~5 seconds, searches in ~150ms
- **100,000 items**: Loads in ~15 seconds, searches in ~200ms
- **1,000,000+ items**: Requires Pinecone upgrade, searches in ~300ms

All timing estimates are for the Pinecone free tier.

## Tips

1. **Start small**: Process 1000 items first to test everything works
2. **Filter by aesthetic**: Higher scores = better quality images
3. **Recent seasons**: 2020+ data is typically more complete
4. **Image URLs**: The dataset includes URLs to all runway images
5. **CLIP embeddings**: Dataset includes pre-computed image embeddings if you want multimodal search later!

## Questions?

Check the main [README](../README.md) or [DEPLOYMENT_GUIDE](../DEPLOYMENT_GUIDE.md) for setup help.
