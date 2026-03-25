from fastmcp import FastMCP
import os

# Creăm serverul MCP
mcp = FastMCP("My MCP server")

# Sandbox folder
SANDBOX_FOLDER = os.environ.get("SANDBOX_FOLDER", "/app/test_data")
os.makedirs(SANDBOX_FOLDER, exist_ok=True)


def ensure_path_inside_sandbox(rel_path: str) -> str:
    """Verifică că path-ul e în sandbox"""
    abs_target = os.path.abspath(os.path.join(SANDBOX_FOLDER, rel_path))
    root_folder = os.path.abspath(SANDBOX_FOLDER)
    
    # Verifică că path-ul este în sandbox (permite și fișiere direct în root)
    if not (abs_target.startswith(root_folder + os.sep) or abs_target == root_folder):
        raise ValueError("Acces interzis in afara SANDBOX_FOLDER")
    return abs_target


@mcp.tool()
def get_file_content(file_path: str) -> str:
    """Citește conținutul unui fișier"""
    try:
        target_file = ensure_path_inside_sandbox(file_path)
        
        if not os.path.exists(target_file):
            return f"Error: File '{file_path}' does not exist."
        
        if not os.path.isfile(target_file):
            return f"Error: '{file_path}' is not a file."
        
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
            return f"File: {file_path}\nSize: {len(content)} characters\n\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def list_directory(dir_path: str) -> str:
    """Listează fișierele și directoarele recursiv"""
    try:
        target_dir = ensure_path_inside_sandbox(dir_path)
        
        if not os.path.isdir(target_dir):
            return f"Error: '{dir_path}' is not a directory."
        
        result = []
        result.append("=" * 60)
        result.append(f"  Continutul directorului: {dir_path}")
        result.append("=" * 60)
        result.append("")
        
        def build_tree(directory, prefix="", is_last=True):
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
        
        result.append(f"[DIR]  {os.path.basename(target_dir)}/")
        result.extend(build_tree(target_dir))
        
        total_files = sum([len(files) for r, d, files in os.walk(target_dir)])
        total_dirs = sum([len(dirs) for r, dirs, f in os.walk(target_dir)])
        
        result.append("")
        result.append("=" * 60)
        result.append(f"  Total: {total_files} fisiere, {total_dirs} directoare")
        result.append("=" * 60)
        
        return "\n".join(result)
    except Exception as e:
        return f"Error listing directory: {str(e)}"


if __name__ == "__main__":
    print(f"Starting MCP Server...")
    print(f"Sandbox folder: {SANDBOX_FOLDER}")
    print(f"Server will listen on http://0.0.0.0:8001")
    
    # Pornim serverul cu SSE transport (HTTP streaming)
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
