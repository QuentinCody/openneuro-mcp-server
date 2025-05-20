# OpenNeuro MCP Server

## License and Citation

This project is available under the MIT License with an Academic Citation Requirement. This means you can freely use, modify, and distribute the code, but any academic or scientific publication that uses this software must provide appropriate attribution.

### For academic/research use:
If you use this software in a research project that leads to a publication, presentation, or report, you **must** cite this work according to the format provided in [CITATION.md](CITATION.md).

### For commercial/non-academic use:
Commercial and non-academic use follows the standard MIT License terms without the citation requirement.

By using this software, you agree to these terms. See [LICENSE.md](LICENSE.md) for the complete license text.Model Context Protocol (MCP) Server for the OpenNeuro GraphQL API.

## Overview

This server provides MCP tools to interact with the OpenNeuro GraphQL API, allowing AI agents to easily access and manipulate neuroimaging datasets on OpenNeuro.

## Installation

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the server:

```bash
python mcp_openneuro.py
```

### Claude Desktop Configuration

To use this MCP server with Claude Desktop, add the following to your `claude_desktop_config.json` file (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "openneuro": {
      "command": "/path/to/your/venv/bin/python",
      "args": [
        "/path/to/your/openneuro-mcp-server/mcp_openneuro.py"
      ],
      "options": {
        "cwd": "/path/to/your/openneuro-mcp-server"
      }
    }
  }
}
```

Replace `/path/to/your/` with the actual path to your installation.

### Available Tools

#### openneuro_graphql

Execute any GraphQL query against the OpenNeuro API.

Example usage in your AI agent's code:

```python
result = await mcp.invoke("openneuro_graphql", {
    "query": "{ datasets(first: 5) { edges { node { id name } } } }"
})
```

## Example Queries

### Listing Datasets

```graphql
{
  datasets(first: 10) {
    edges {
      node {
        id
        name
        created
      }
    }
  }
}
```

### Getting a Specific Dataset

```graphql
{
  dataset(id: "ds000001") {
    id
    name
    public
    created
    metadata {
      modalities
    }
    latestSnapshot {
      tag
      created
    }
  }
}
```

### Search by Modality

```graphql
{
  datasets(first: 5, modality: "MRI") {
    edges {
      node {
        id
        name
        created
      }
    }
  }
}
```

### Dataset Metadata and Summary

```graphql
{
  dataset(id: "ds000001") {
    id
    name
    metadata {
      modalities
      dataProcessed
      species
    }
    latestSnapshot {
      summary {
        subjects
        sessions
        tasks
        modalities
        totalFiles
        size
      }
    }
  }
}
```

## Using Variables

Some queries require variables. Here's an example:

```python
query = """
query GetDataset($id: ID!) {
  dataset(id: $id) {
    id
    name
    public
  }
}
"""

variables = {
    "id": "ds000001"
}

result = await mcp.invoke("openneuro_graphql", {
    "query": query,
    "variables": variables
})
```

## Testing

Several test scripts are included to demonstrate usage:

- `test_query.py` - Basic listing of datasets
- `test_dataset_query.py` - Detailed information about a specific dataset
- `test_search_query.py` - Search functionality example
- `test_datasets_with_modality.py` - Filter datasets by modality

Run any test script:

```bash
python test_query.py
```

## Development

To add more tools or functionality, modify the `mcp_openneuro.py` file and add new methods with the `@mcp.tool()` decorator.

## License

MIT