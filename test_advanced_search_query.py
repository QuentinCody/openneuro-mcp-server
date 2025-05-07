import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_advanced_search_query():
    # Run an advanced search query with variables
    query = """
    query AdvancedSearch($query: JSON!, $first: Int) {
      advancedSearch(query: $query, first: $first) {
        edges {
          node {
            id
            name
            created
            latestSnapshot {
              tag
            }
            metadata {
              modalities
            }
          }
        }
      }
    }
    """
    
    variables = {
        "query": {"text": "fMRI"},
        "first": 5
    }
    
    result = await openneuro_graphql(query, variables)
    print("Advanced Search Query Result:")
    print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_advanced_search_query()) 