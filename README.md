# ADK MCP Ollama System

Sistem complet de agenți AI cu interfață web, server MCP (Model Context Protocol) și model local Ollama, containerizat cu Docker.

## 📋 Descriere

Acest proiect integrează:
- **ADK Web UI** - Interfață web Angular pentru interacțiune cu agentul
- **MCP Server** - Server FastMCP cu tool-uri pentru operații pe fișiere
- **Ollama** - Model local de limbaj (llama3.2:3b)
- **Agent Sysadmin** - Agent AI care folosește tool-urile MCP pentru administrare sistem

## 🏗️ Arhitectură

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

## 🚀 Pornire Rapidă

### Cerințe
- Docker & Docker Compose
- ~4GB spațiu liber (pentru modelul Ollama)

### Instalare și Rulare

```bash
# Clonează repository-ul
git clone <repo-url>
cd <repo-name>

# Pornește toate containerele
cd proiect
docker-compose up -d

# Verifică statusul
docker ps

# Vezi logs
docker-compose logs -f
```

### Accesare

- **ADK Web Interface**: http://localhost:8082
- **Ollama API**: http://localhost:11434
- **MCP Server**: http://localhost:8001/sse

## 🧪 Testare

1. Deschide browser la http://localhost:8082
2. Selectează agentul "sysadmin_agent"
3. Trimite un mesaj: "Listează fișierele din directorul curent"
4. Agentul va folosi tool-urile MCP pentru a răspunde

## 📁 Structura Proiectului

```
.
├── adk-web/                    # Frontend Angular
│   ├── src/                    # Cod sursă Angular
│   ├── package.json
│   └── angular.json
│
└── proiect/                    # Backend Python
    ├── my_server_http.py       # MCP Server (FastMCP cu SSE)
    ├── agent_auth.py           # Configurare agent ADK
    ├── sitecustomize.py        # Bypass tiktoken pentru Docker
    ├── bypass_tiktoken.py      # Backup bypass
    ├── docker-compose.yml      # Orchestrare containere
    ├── Dockerfile.mcp          # Container MCP Server
    ├── Dockerfile.adk          # Container ADK Web
    ├── Dockerfile.ollama       # Container Ollama
    ├── requirements.txt        # Dependențe Python
    └── README_DOCKER.md        # Documentație detaliată Docker
```

## 🐳 Containere Docker

| Container | Port | Descriere |
|-----------|------|-----------|
| adk-web | 8082 | Interfață web pentru agent |
| mcp-server | 8001 | Server MCP cu tool-uri pentru fișiere |
| ollama | 11434 | Model local llama3.2:3b |

## 🛠️ Tool-uri MCP Disponibile

- **list_directory** - Listează fișiere și directoare recursiv
- **get_file_content** - Citește conținutul unui fișier

## 🔧 Configurare

### Variabile de Mediu

Creează un fișier `.env` în root (opțional):

```bash
MCP_API_KEY=your-secret-key-here
```

### Customizare Agent

Editează `proiect/agent_auth.py` pentru a modifica:
- Instrucțiunile agentului
- Tool-urile disponibile
- Modelul de limbaj folosit

## 📚 Documentație Suplimentară

- [README_DOCKER.md](proiect/README_DOCKER.md) - Ghid complet Docker setup
- [INSTRUCTIUNI_TESTARE.md](proiect/INSTRUCTIUNI_TESTARE.md) - Ghid detaliat de testare

## 🔍 Troubleshooting

### Container nu pornește
```bash
docker-compose logs <container-name>
```

### Rebuild complet
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Verificare comunicare între containere
```bash
docker exec -it adk-web ping ollama
docker exec -it adk-web ping mcp-server
```

## 🛑 Oprire

```bash
# Stop containere
docker-compose down

# Stop și șterge volumes
docker-compose down -v
```

## 📝 Note Tehnice

### Rezolvarea Problemei Tiktoken

Docker container-ul nu poate descărca encodings tiktoken de pe internet din cauza SSL errors. Am implementat un bypass complet prin:
- `sitecustomize.py` - se execută automat la pornirea Python
- Mock-uiește toate apelurile tiktoken
- Pentru modele locale Ollama, tiktoken nu este necesar

### Volumes Docker

- **ollama-data** - Păstrează modelul llama3.2:3b descărcat (~2GB)
- **test_data** - Director pentru testare (mount din proiect)

## 🤝 Contribuții

Contribuțiile sunt binevenite! Pentru modificări majore, deschide mai întâi un issue pentru a discuta ce ai dori să schimbi.

## 📄 Licență

[Apache 2.0](LICENSE)

## 🔗 Link-uri Utile

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Ollama](https://ollama.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Dezvoltat cu ❤️ folosind Google Agent Development Kit**
