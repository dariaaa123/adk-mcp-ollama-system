
# ADK MCP Ollama System

A complete AI agent system with web interface, MCP (Model Context Protocol) server, and local Ollama model, containerized with Docker.

## Description

This project integrates:

* **ADK Web UI** - Angular web interface for interacting with the agent
* **MCP Server** - FastMCP server with tools for file operations
* **Ollama** - Local language model (llama3.2:3b)
* **Sysadmin Agent** - AI agent that uses MCP tools for system administration

## Architecture

```
┌─────────────┐
│  Browser    │
│ :8082       │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────────┐
│  ADK Web        │─────▶│  Ollama          │
│  (Angular)      │      │  llama3.2:3b     │
└──────┬──────────┘      └──────────────────┘
       │                  Port: 11434
       │ SSE
       ▼
┌─────────────────┐
│ MCP Server      │
│ (FastMCP)       │
└──────┬──────────┘
       │ Port: 8001
       ▼
┌─────────────────┐
│ File System     │
└─────────────────┘
```

## Quick Start

### Requirements

* Docker & Docker Compose
* ~4GB free space (for the Ollama model)

### Installation and Run

```bash
# Clone the repository
git clone <repo-url>
cd <repo-name>

# Start all containers
cd proiect
docker-compose up -d

# Check status
docker ps

# View logs
docker-compose logs -f
```

### Access

* **ADK Web Interface**: [http://localhost:8082](http://localhost:8082)
* **Ollama API**: [http://localhost:11434](http://localhost:11434)
* **MCP Server**: [http://localhost:8001/sse](http://localhost:8001/sse)

## Testing

1. Open browser at [http://localhost:8082](http://localhost:8082)
2. Select the "sysadmin_agent" agent
3. Send a message: "List files in the current directory"
4. The agent will use MCP tools to respond

## Project Structure

```
.
├── adk-web/                    # Angular frontend
│   ├── src/                    # Angular source code
│   ├── package.json
│   └── angular.json
│
└── proiect/                    # Python backend
    ├── my_server_http.py       # MCP Server (FastMCP with SSE)
    ├── agent_auth.py           # ADK agent configuration
    ├── sitecustomize.py        # tiktoken bypass for Docker
    ├── bypass_tiktoken.py      # Backup bypass
    ├── docker-compose.yml      # Container orchestration
    ├── Dockerfile.mcp          # MCP Server container
    ├── Dockerfile.adk          # ADK Web container
    ├── Dockerfile.ollama       # Ollama container
    ├── requirements.txt        # Python dependencies
    └── README_DOCKER.md        # Detailed Docker documentation
```

## Docker Containers

| Container  | Port  | Description                 |
| ---------- | ----- | --------------------------- |
| adk-web    | 8082  | Web interface for the agent |
| mcp-server | 8001  | MCP server with file tools  |
| ollama     | 11434 | Local model llama3.2:3b     |

## Available MCP Tools

* **list_directory** - Lists files and directories recursively
* **get_file_content** - Reads the contents of a file

## Configuration

### Environment Variables

Create a `.env` file in the root (optional):

```bash
MCP_API_KEY=your-secret-key-here
```

### Agent Customization

Edit `proiect/agent_auth.py` to modify:

* Agent instructions
* Available tools
* Language model used

## Technical Notes

### Fixing the Tiktoken Issue

The Docker container cannot download tiktoken encodings from the internet due to SSL errors. A complete bypass has been implemented using:

* `sitecustomize.py` - automatically executed at Python startup
* Mocks all tiktoken calls
* For local Ollama models, tiktoken is not required

### Docker Volumes

* **ollama-data** - Stores the downloaded llama3.2:3b model (~2GB)
* **test_data** - Directory for testing (mounted from the project)

