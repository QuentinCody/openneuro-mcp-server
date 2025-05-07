import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_dataset_query():
    # Run a query to get details about a specific dataset
    query = """
    {
      dataset(id: "ds000001") {
        id
        name
        public
        created
        modalities: metadata {
          modalities
        }
        latestSnapshot {
          tag
          created
          summary {
            subjects
            sessions
            tasks
            modalities
          }
        }
      }
    }
    """
    
    result = await openneuro_graphql(query)
    print("Dataset Query Result:")
    print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_dataset_query()) 