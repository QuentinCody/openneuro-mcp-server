import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_search_query():
    # Run a search query to find datasets related to fMRI
    query = """
    {
      search(q: "fMRI", first: 5) {
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
    
    result = await openneuro_graphql(query)
    print("Search Query Result:")
    print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_search_query()) 