from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import SseConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
import os

# Cheia de autentificare - trebuie să fie aceeași cu cea din MCP server
API_KEY = os.getenv("MCP_API_KEY", "my-super-secret-key-2024")

# URL-ul MCP server-ului
MCP_URL = "http://localhost:8001/sse"

# Creăm toolset MCP cu autentificare
params = SseConnectionParams(
    url=MCP_URL,
    headers={
        "X-API-Key": API_KEY  # Adăugăm header-ul de autentificare
    }
)
toolset = McpToolset(connection_params=params)

# Configurăm modelul Ollama
model = LiteLlm(
    model="ollama_chat/llama3.2:3b",
    api_base="http://localhost:11434"
)

# Creăm agentul cu autentificare
root_agent = Agent(
    name="sysadmin_agent_secure",
    model=model,
    description=(
        "Agent sysadmin securizat care folosește serverul FastMCP cu autentificare "
        "pentru listarea fișierelor și citirea conținutului."
    ),
    instruction="""Tu ești un agent sysadmin securizat. TREBUIE să folosești tool-urile disponibile pentru a răspunde la întrebări.

IMPORTANT:
- Pentru a lista fișiere dintr-un director, TREBUIE să apelezi tool-ul list_directory cu calea completă
- Pentru a citi conținutul unui fișier, TREBUIE să apelezi tool-ul get_file_content cu calea completă
- NU inventa sau ghici conținutul - folosește DOAR informațiile returnate de tool-uri
- Răspunde în limba română, clar și concis
- Toate comunicările cu serverul MCP sunt autentificate și securizate""",
    tools=[toolset],
)
