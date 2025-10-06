from importlib import import_module
from pathlib import Path

__app_name__ = "EvolutivoFW MCP"
__version__ = "1.0.0"
__author__ = "Joe Bordes"
__license__ = "Apache 2.0"

def register_all(mcp):
    tools_dir = Path(__file__).parent
    for py_file in tools_dir.glob("*.py"):
        if py_file.stem == "__init__":
            continue
        module = import_module(f".{py_file.stem}", package="tools")
        if hasattr(module, "register"):
            module.register(mcp)
