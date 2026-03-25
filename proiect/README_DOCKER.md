# Docker Setup pentru Proiect MCP + Ollama + ADK Web

## Componente

Acest proiect conține 3 containere Docker:

1. **Ollama** - Server LLM local cu modelul llama3.2:3b (port 11434)
2. **MCP Server** - Server MCP cu HTTP streaming/SSE (port 8001)
3. **ADK Web** - Interfață web pentru agent (port 8082)

## Pornire Rapidă

```powershell
# Pornește toate containerele
docker-compose up -d

# Verifică statusul
docker ps

# Vezi logs
docker logs ollama-llama3.2
docker logs mcp-server
docker logs adk-web
```

## Accesare

- **ADK Web Interface**: http://localhost:8082
- **Ollama API**: http://localhost:11434
- **MCP Server**: http://localhost:8001/sse

## Testare

### 1. Test Ollama
```powershell
curl http://localhost:11434/api/generate -d '{\"model\":\"llama3.2:3b\",\"prompt\":\"Hello\"}'
```

### 2. Test MCP Server
Serverul MCP folosește SSE (Server-Sent Events) și poate fi testat prin ADK Web interface.

### 3. Test ADK Web
Deschide browser la http://localhost:8082 și:
1. Selectează agentul "sysadmin_agent"
2. Trimite un mesaj: "Listează fișierele din directorul curent"
3. Agentul va folosi tool-urile MCP pentru a răspunde

## Rezolvarea Problemei Tiktoken

**Problema**: LiteLLM (folosit de google-adk) încearcă să descarce encodings tiktoken de pe internet la runtime, dar Docker container-ul nu poate accesa Azure blob storage din cauza SSL errors.

**Soluția**: Am implementat un bypass complet pentru tiktoken folosind monkey patching:
- Fișierul `sitecustomize.py` se execută AUTOMAT la pornirea Python (înainte de orice import)
- Creează un modul fake tiktoken și îl injectează în `sys.modules`
- Toate apelurile tiktoken sunt mock-uite și returnează valori dummy
- Pentru Ollama (model local), tiktoken nu este necesar pentru funcționalitate

**Fișiere cheie**:
- `sitecustomize.py` - bypass global (se execută automat)
- `bypass_tiktoken.py` - backup bypass
- `Dockerfile.adk` - copiază sitecustomize.py în site-packages

## Structura Fișierelor

```
proiect/
├── docker-compose.yml          # Configurare pentru toate containerele
├── Dockerfile.ollama           # Ollama cu llama3.2:3b
├── Dockerfile.mcp              # MCP Server cu FastMCP
├── Dockerfile.adk              # ADK Web cu agent
├── my_server_http.py           # Implementare MCP Server (SSE)
├── agent_auth.py               # Configurare agent ADK
├── sitecustomize.py            # Bypass pentru tiktoken (SOLUȚIA!)
├── bypass_tiktoken.py          # Backup bypass
└── test_data/                  # Date pentru testare MCP
```

## Comenzi Utile

```powershell
# Rebuild un singur container
docker-compose build adk-web
docker-compose up -d adk-web

# Stop toate containerele
docker-compose down

# Stop și șterge volumes
docker-compose down -v

# Vezi logs în timp real
docker-compose logs -f adk-web

# Intră în container pentru debugging
docker exec -it adk-web /bin/bash
```

## Arhitectura Sistemului

```
┌─────────────┐
│  Browser    │
│ :8082       │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────────┐
│  ADK Web        │─────▶│  Ollama          │
│  (Docker)       │      │  (Docker)        │
└──────┬──────────┘      └──────────────────┘
       │                  Port: 11434
       │ SSE              Model: llama3.2:3b
       ▼
┌─────────────────┐
│ MCP Server      │
│ (Docker + SSE)  │
└──────┬──────────┘
       │ Port: 8001
       ▼
┌─────────────────┐
│ test_data/      │
└─────────────────┘
```

## Volumele Docker

- **ollama-data**: Păstrează modelul llama3.2:3b descărcat (~2GB)
- **test_data**: Director pentru testare (mount din proiect)

## Porturile Expuse

| Port | Serviciu | Descriere |
|------|----------|-----------|
| 8001 | MCP Server | HTTP SSE endpoint |
| 8082 | ADK Web | Interfață web pentru agent |
| 11434 | Ollama | API pentru modelul de limbaj |

