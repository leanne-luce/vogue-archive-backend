"""
Vogue Archive Search Logic with CLIP
"""
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

class VogueArchiveSearch:
    def __init__(self, api_key, index_name, environment):
        """Initialize the search engine with CLIP model for better fashion understanding"""
        # Using CLIP for fashion-aware embeddings (512 dimensions)
        self.model = SentenceTransformer('clip-ViT-B-32')
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)

    def search(self, query, top_k=10, filters=None):
        """
        Search the Vogue archive

        Args:
            query (str): Search query
            top_k (int): Number of results to return
            filters (dict): Optional metadata filters

        Returns:
            list: Search results with metadata
        """
        # Generate query embedding
        query_embedding = self.model.encode(query).tolist()

        # Build filter query for Pinecone
        pinecone_filter = self._build_filter(filters) if filters else None

        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=pinecone_filter
        )

        # Format results
        formatted_results = []
        for match in results['matches']:
            formatted_results.append({
                'id': match['id'],
                'score': float(match['score']),
                'metadata': match['metadata']
            })

        return formatted_results

    def _build_filter(self, filters):
        """Build Pinecone filter query from filters dict"""
        pinecone_filter = {}

        # Year filters
        if 'year' in filters:
            pinecone_filter['year'] = {'$eq': filters['year']}

        if 'year_range' in filters:
            pinecone_filter['year'] = {
                '$gte': filters['year_range']['min'],
                '$lte': filters['year_range']['max']
            }

        # Designer filter
        if 'designer' in filters:
            pinecone_filter['designer'] = {'$eq': filters['designer']}

        # Category filter (e.g., "Ready-to-Wear", "Couture")
        if 'category' in filters:
            pinecone_filter['category'] = {'$eq': filters['category']}

        # Season filter (e.g., "Spring", "Fall")
        if 'season' in filters:
            pinecone_filter['season'] = {'$eq': filters['season']}

        # City filter (e.g., "Paris", "Milan", "New York")
        if 'city' in filters:
            pinecone_filter['city'] = {'$eq': filters['city']}

        # Aesthetic score filter (minimum quality)
        if 'min_aesthetic' in filters:
            pinecone_filter['aesthetic_score'] = {'$gte': filters['min_aesthetic']}

        return pinecone_filter

    def get_stats(self):
        """Get index statistics"""
        stats = self.index.describe_index_stats()
        return {
            'total_vectors': stats.get('total_vector_count', 0),
            'dimension': stats.get('dimension', 384),
            'index_fullness': stats.get('index_fullness', 0.0)
        }
