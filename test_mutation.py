import asyncio
import json
from mcp_openneuro import openneuro_graphql

async def test_mutation():
    """
    Note: This mutation requires authentication and would only work
    when run with proper credentials.
    
    This is just a demonstration of how mutations would be structured.
    """
    # Example mutation to star a dataset
    query = """
    mutation StarDataset($datasetId: ID!) {
      starDataset(datasetId: $datasetId) {
        starred
        newStar {
          userId
          datasetId
        }
      }
    }
    """
    
    variables = {
        "datasetId": "ds000001"
    }
    
    print("Attempting mutation (note: this will likely fail without authentication):")
    print(f"Query: {query}")
    print(f"Variables: {variables}")
    
    # In a real scenario with authentication, you would execute this:
    # result = await openneuro_graphql(query, variables)
    # print(json.dumps(json.loads(result), indent=2))
    
    print("\nTo properly execute mutations, you would need to:")
    print("1. Set up authentication in the MCP server")
    print("2. Add authentication headers to the GraphQL requests")
    print("3. Include proper credentials for the authenticated user")

if __name__ == "__main__":
    asyncio.run(test_mutation()) 