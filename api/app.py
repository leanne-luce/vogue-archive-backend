"""
Vogue Archive Search API
Deploy to Render.com free tier
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from search import VogueArchiveSearch

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native

# Initialize search engine
search_engine = VogueArchiveSearch(
    api_key=os.environ.get('PINECONE_API_KEY'),
    index_name=os.environ.get('PINECONE_INDEX_NAME', 'vogue-archive'),
    environment=os.environ.get('PINECONE_ENVIRONMENT', 'us-east-1-aws')
)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Vogue Archive Search API',
        'version': '1.0.0'
    })

@app.route('/search', methods=['POST'])
def search():
    """
    Search the Vogue archive

    Request body:
    {
        "query": "elegant evening gowns from the 1950s",
        "top_k": 10,
        "filters": {
            "year": 1950,
            "designer": "Christian Dior"
        }
    }
    """
    try:
        data = request.get_json()

        # Validate request
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required field: query'
            }), 400

        query = data['query']
        top_k = data.get('top_k', 10)
        filters = data.get('filters', {})

        # Perform search
        results = search_engine.search(
            query=query,
            top_k=top_k,
            filters=filters
        )

        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get index statistics"""
    try:
        stats = search_engine.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
