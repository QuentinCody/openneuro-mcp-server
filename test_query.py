import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_query():
    # Run a simple query to get a few datasets
    query = """
    {
      datasets(first: 3) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    
    result = await openneuro_graphql(query)
    print("Query result:")
    print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_query()) 