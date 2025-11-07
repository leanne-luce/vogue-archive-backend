# API Documentation

Base URL: `https://your-app.onrender.com`

## Endpoints

### GET /
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Vogue Archive Search API",
  "version": "1.0.0"
}
```

### POST /search
Search the Vogue archive with semantic search.

**Request Body:**
```json
{
  "query": "elegant evening gowns from the 1950s",
  "top_k": 10,
  "filters": {
    "year": 1955,
    "designer": "Christian Dior",
    "category": "Evening Wear"
  }
}
```

**Parameters:**
- `query` (string, required): Search query in natural language
- `top_k` (integer, optional): Number of results to return (default: 10, max: 100)
- `filters` (object, optional): Metadata filters to narrow results

**Supported Filters:**
- `year` (integer): Exact year match
- `designer` (string): Designer name
- `category` (string): Category (e.g., "Evening Wear", "Day Wear")
- `year_range` (object): Range of years `{"min": 1950, "max": 1959}`

**Response:**
```json
{
  "query": "elegant evening gowns from the 1950s",
  "results": [
    {
      "id": "vogue_1955_03_p42",
      "score": 0.892,
      "metadata": {
        "year": 1955,
        "month": 3,
        "page": 42,
        "description": "Christian Dior evening gown with full skirt and fitted bodice",
        "image_url": "https://example.com/image1.jpg",
        "designer": "Christian Dior",
        "category": "Evening Wear"
      }
    }
  ],
  "count": 10
}
```

**Response Fields:**
- `id` (string): Unique identifier for the record
- `score` (float): Similarity score (0-1, higher is better)
- `metadata` (object): All metadata associated with the record

### GET /stats
Get Pinecone index statistics.

**Response:**
```json
{
  "total_vectors": 10000,
  "dimension": 384,
  "index_fullness": 0.01
}
```

## Error Responses

### 400 Bad Request
Missing required fields or invalid parameters.

```json
{
  "error": "Missing required field: query"
}
```

### 500 Internal Server Error
Server error or Pinecone API error.

```json
{
  "error": "Pinecone connection failed"
}
```

## Rate Limits

Render free tier:
- No explicit rate limits
- Cold starts after 15 minutes of inactivity (~30 seconds delay)

## Examples

### Basic Search
```bash
curl -X POST https://your-app.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vintage Chanel suits",
    "top_k": 5
  }'
```

### Search with Filters
```bash
curl -X POST https://your-app.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "summer dresses",
    "top_k": 10,
    "filters": {
      "year_range": {"min": 1960, "max": 1969},
      "category": "Day Wear"
    }
  }'
```

### React Native Example
```typescript
const searchVogue = async (query: string) => {
  const response = await fetch('https://your-app.onrender.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      top_k: 10
    })
  });

  const data = await response.json();
  return data.results;
};
```
