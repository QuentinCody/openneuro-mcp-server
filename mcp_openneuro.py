import os
import httpx
import json
import sys
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Initialize MCP Server
mcp = FastMCP("openneuro", version="0.1.0")
print("OpenNeuro MCP Server initialized.", file=sys.stderr)

# OpenNeuro GraphQL API Configuration
GRAPHQL_ROOT = 'https://openneuro.org/crn/graphql'

async def execute_graphql_query(query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Executes a GraphQL query against OpenNeuro's API.
    Handles error checking and response formatting.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MCPOpenNeuroServer/0.1.0"
        }
        
        data = {
            "query": query
        }
        
        if variables:
            data["variables"] = variables
        
        print(f"Debug - Making GraphQL request to: {GRAPHQL_ROOT}", file=sys.stderr)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GRAPHQL_ROOT,
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            print(f"Debug - API response status: {response.status_code}", file=sys.stderr)
            
            response.raise_for_status()
            result = response.json()
            
            return result
    except httpx.RequestError as e:
        print(f"HTTP Request Error: {e}", file=sys.stderr)
        return {"errors": [{"message": f"HTTP Request Error connecting to OpenNeuro: {e}"}]}
    except httpx.HTTPStatusError as e:
        print(f"HTTP Status Error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        error_detail = f"HTTP Status Error: {e.response.status_code}"
        try:
            # Try to parse error response if JSON
            err_resp = e.response.json()
            if "errors" in err_resp:
                error_detail += f" - {err_resp['errors'][0]['message']}"
            elif "error" in err_resp and "message" in err_resp["error"]:
                error_detail += f" - {err_resp['error']['message']}"
            else:
                error_detail += f" - Response: {e.response.text[:200]}"
        except json.JSONDecodeError:
            error_detail += f" - Response: {e.response.text[:200]}"
        
        return {"errors": [{"message": error_detail}]}
    except Exception as e:
        print(f"Generic Error during OpenNeuro request: {e}", file=sys.stderr)
        return {"errors": [{"message": f"An unexpected error occurred: {e}"}]}

@mcp.tool()
async def openneuro_graphql(query: str, variables: Dict[str, Any] = None) -> str:
    """
    Execute any GraphQL query against the OpenNeuro API.
    
    This single flexible tool allows executing any valid GraphQL query against the OpenNeuro API,
    leveraging GraphQL's introspection capabilities to discover the schema and available operations.
    
    Examples of queries:
    - Get dataset details: {dataset(id: "ds000001") {id name public}}
    - List datasets: {datasets(first: 10) {edges {node {id name}}}}
    - Search datasets: {search(q: "fMRI", first: 10) {edges {node {id name}}}}
    - Advanced search: {advancedSearch(query: {}, first: 10) {edges {node {id name}}}}
    
    Args:
        query: The GraphQL query to execute (required)
        variables: Optional dictionary of variables for the GraphQL query
        
    Returns:
        JSON string containing the query results
    """
    print(f"Executing openneuro_graphql with query: {query[:100]}...", file=sys.stderr)
    
    result = await execute_graphql_query(query, variables)
    
    return json.dumps(result)

if __name__ == "__main__":
    print("Running OpenNeuro MCP server via stdio...", file=sys.stderr)
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"Fatal error running MCP server: {e}", file=sys.stderr) 