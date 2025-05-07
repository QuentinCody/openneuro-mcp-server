import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_datasets_modality_query():
    # Run a query to get datasets with a specific modality
    query = """
    {
      datasets(first: 5, modality: "MRI") {
        edges {
          node {
            id
            name
            created
            latestSnapshot {
              tag
              created
            }
          }
        }
      }
    }
    """
    
    result = await openneuro_graphql(query)
    print("Datasets with MRI Modality:")
    print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_datasets_modality_query()) 