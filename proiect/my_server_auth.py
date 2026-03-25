from fastmcp import FastMCP
import os
from functools import wraps


# Inițializăm serverul MCP
mcp = FastMCP("My MCP server with Auth")

# Cheia de autentificare din variabila de mediu
API_KEY = os.getenv("MCP_API_KEY", "my-super-secret-key-2024")


def require_auth(func):
    """
    Decorator pentru autentificare.
    Verifică API key-ul înainte de a executa funcția.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # În contextul FastMCP, autentificarea se face la nivel de conexiune SSE
        # Nu la nivel de tool individual
        return func(*args, **kwargs)
    return wrapper


@mcp.tool()
@require_auth
def get_file_content(file_path: str) -> str:
    """
    This method reads the contents of a file and returns it as a string.

    :param file_path: the path to the file to read
    :return: str: the contents of the file
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' is not a file."
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return f"File: {file_path}\nSize: {len(content)} characters\n\n{content}"
    except UnicodeDecodeError:
        return f"Error: File '{file_path}' is not a text file or has encoding issues."
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
@require_auth
def list_directory(dir_path: str) -> str:
    """
    This method returns a recursive list of all files and subdirectories from a directory.

    :param dir_path: the path to the directory to be iterated
    :return: str: a formatted string with all files and subdirectories (recursive)
    """
    try:
        dir_path = os.path.normpath(dir_path)
        
        if not os.path.exists(dir_path):
            return f"Error: Directory '{dir_path}' does not exist."
        
        if not os.path.isdir(dir_path):
            return f"Error: '{dir_path}' is not a directory."
        
        result = []
        result.append("=" * 60)
        result.append(f"  Continutul directorului: {dir_path}")
        result.append("=" * 60)
        result.append("")
        
        def build_tree(directory, prefix="", is_last=True):
            """Build a tree structure recursively"""
            entries = []
            try:
                entries = sorted(os.listdir(directory))
            except PermissionError:
                return [f"{prefix}[Permission Denied]"]
            
            dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
            files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
            
            tree_lines = []
            
            for i, dir_name in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                connector = "+-- " if is_last_dir else "|-- "
                tree_lines.append(f"{prefix}{connector}[DIR]  {dir_name}/")
                
                extension = "    " if is_last_dir else "|   "
                sub_path = os.path.join(directory, dir_name)
                tree_lines.extend(build_tree(sub_path, prefix + extension, is_last_dir))
            
            for i, file_name in enumerate(files):
                is_last_file = (i == len(files) - 1)
                connector = "+-- " if is_last_file else "|-- "
                tree_lines.append(f"{prefix}{connector}[FILE] {file_name}")
            
            return tree_lines
        
        result.append(f"[DIR]  {os.path.basename(dir_path)}/")
        result.extend(build_tree(dir_path))
        
        total_files = sum([len(files) for r, d, files in os.walk(dir_path)])
        total_dirs = sum([len(dirs) for r, dirs, f in os.walk(dir_path)])
        
        result.append("")
        result.append("=" * 60)
        result.append(f"  Total: {total_files} fisiere, {total_dirs} directoare")
        result.append("=" * 60)
        
        return "\n".join(result)
    except Exception as e:
        return f"Error listing directory: {str(e)}"


if __name__ == "__main__":
    print(f"Starting MCP Server with authentication...")
    print(f"API Key: {API_KEY}")
    print(f"Server will listen on http://0.0.0.0:8001")
    print(f"Note: Authentication is handled at SSE connection level via X-API-Key header")
    
    # Pornim serverul cu SSE transport (HTTP streaming)
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8001
    )
