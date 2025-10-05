from importlib import import_module
from pathlib import Path

def register_all(mcp):
    tools_dir = Path(__file__).parent
    for py_file in tools_dir.glob("*.py"):
        if py_file.stem == "__init__":
            continue
        module = import_module(f".{py_file.stem}", package="tools")
        if hasattr(module, "register"):
            module.register(mcp)
