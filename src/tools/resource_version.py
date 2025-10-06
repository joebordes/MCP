from mcp.server.fastmcp import FastMCP
from tools import __app_name__, __version__


def register(mcp: FastMCP):

    @mcp.resource("resource://version")
    def get_version() -> str:
        """Provides version information about the MCP server."""
        return f"Hello from {__app_name__} v{__version__}. Welcome to the next generation of business applications!"
