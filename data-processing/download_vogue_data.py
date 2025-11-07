"""
Download and prepare Vogue Runway dataset from Internet Archive
https://archive.org/details/VogueRunway_dataset

This script downloads a subset of the dataset and prepares it for embedding generation.
"""

import os
import json
import pandas as pd
import requests
from pathlib import Path
from tqdm import tqdm

# Configuration
ARCHIVE_BASE_URL = "https://archive.org/download/VogueRunway_dataset"
PARQUET_FILE = "VogueRunway.parquet"
OUTPUT_DIR = Path("vogue_data")
MAX_ITEMS = 1000  # Adjust this to download more/less items

def download_parquet():
    """Download the metadata parquet file"""
    print("Downloading metadata parquet file...")
    parquet_url = f"{ARCHIVE_BASE_URL}/{PARQUET_FILE}"

    output_path = OUTPUT_DIR / PARQUET_FILE
    output_path.parent.mkdir(exist_ok=True, parents=True)

    response = requests.get(parquet_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as f, tqdm(
        desc=PARQUET_FILE,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

    print(f"✓ Downloaded metadata to {output_path}")
    return output_path

def load_and_filter_metadata(parquet_path, max_items=MAX_ITEMS):
    """Load metadata and select items to download"""
    print(f"\nLoading metadata from {parquet_path}...")
    df = pd.read_parquet(parquet_path)

    print(f"Total items in dataset: {len(df):,}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nSample data:")
    print(df.head())

    # Filter for high-quality items (optional - adjust as needed)
    # You can filter by designer, year, aesthetic score, etc.
    if 'aesthetic' in df.columns:
        # Take items with higher aesthetic scores
        df_filtered = df.nlargest(max_items, 'aesthetic')
        print(f"\nFiltered to top {max_items} items by aesthetic score")
    else:
        # Just take first N items
        df_filtered = df.head(max_items)
        print(f"\nTaking first {max_items} items")

    return df_filtered

def download_images(df, max_downloads=50):
    """
    Download a sample of images from the dataset
    Note: Full dataset is 854GB, so we only download a small sample
    """
    print(f"\n{'='*60}")
    print(f"Downloading {max_downloads} sample images...")
    print(f"{'='*60}\n")

    images_dir = OUTPUT_DIR / "images"
    images_dir.mkdir(exist_ok=True, parents=True)

    downloaded = []

    for idx, row in tqdm(df.head(max_downloads).iterrows(), total=max_downloads):
        try:
            key = row['key']
            filename = row['filename']

            # Determine which shard this image is in
            shard_num = int(str(key)[:3])
            tar_name = f"vogue_runway_{shard_num:03d}.tar"

            # For simplicity, we'll use the direct image URLs from Vogue Runway
            # The actual tar files are 6.7GB each - too large for quick testing

            # Construct filename from metadata
            image_filename = f"{key}.jpg"
            image_path = images_dir / image_filename

            # Skip if already downloaded
            if image_path.exists():
                downloaded.append({
                    'key': key,
                    'local_path': str(image_path),
                    'metadata': row.to_dict()
                })
                continue

            # Note: Direct image download from tar requires extraction
            # For now, we'll work with just metadata
            downloaded.append({
                'key': key,
                'local_path': None,  # Will use metadata only
                'metadata': row.to_dict()
            })

        except Exception as e:
            print(f"Error downloading {key}: {e}")
            continue

    print(f"\n✓ Processed {len(downloaded)} items")
    return downloaded

def prepare_for_embedding(df):
    """
    Prepare the data in the format needed for embedding generation
    """
    print("\nPreparing data for embedding generation...")

    output_file = OUTPUT_DIR / "vogue_runway_prepared.json"

    items = []
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        # Create searchable text from metadata
        description_parts = []

        if pd.notna(row.get('designer')):
            description_parts.append(f"{row['designer']}")
        if pd.notna(row.get('season')) and pd.notna(row.get('year')):
            description_parts.append(f"{row['season']} {row['year']}")
        if pd.notna(row.get('category')):
            description_parts.append(f"{row['category']}")
        if pd.notna(row.get('section')):
            description_parts.append(f"{row['section']}")
        if pd.notna(row.get('city')):
            description_parts.append(f"{row['city']} Fashion Week")

        description = " ".join(description_parts)

        item = {
            "id": f"vogue_runway_{row['key']}",
            "description": description,
            "metadata": {
                "designer": str(row.get('designer', '')),
                "season": str(row.get('season', '')),
                "year": int(row.get('year', 0)) if pd.notna(row.get('year')) else 0,
                "category": str(row.get('category', '')),
                "city": str(row.get('city', '')),
                "section": str(row.get('section', '')),
                "image_url": row.get('url', ''),
                "aesthetic_score": float(row.get('aesthetic', 0)) if pd.notna(row.get('aesthetic')) else 0,
            }
        }
        items.append(item)

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(items, f, indent=2)

    print(f"✓ Saved {len(items)} items to {output_file}")
    print(f"\nSample item:")
    print(json.dumps(items[0], indent=2))

    return output_file

def main():
    """Main execution flow"""
    print("="*60)
    print("Vogue Runway Dataset Downloader")
    print("="*60)

    # Step 1: Download metadata
    parquet_path = download_parquet()

    # Step 2: Load and filter metadata
    df = load_and_filter_metadata(parquet_path, max_items=MAX_ITEMS)

    # Step 3: Prepare for embedding (metadata only for now)
    output_file = prepare_for_embedding(df)

    print("\n" + "="*60)
    print("✓ Done! Next steps:")
    print("="*60)
    print(f"1. Open the Colab notebook: data-processing/process_vogue_data.ipynb")
    print(f"2. Upload {output_file}")
    print(f"3. Run all cells to generate embeddings and upload to Pinecone")
    print("="*60)

if __name__ == "__main__":
    main()
