from mcp.server.fastmcp import FastMCP
from tools import register_all

mcp = FastMCP("EvolutivoFW MCP", "1.0.0")

# Register all tools dynamically
register_all(mcp)

if __name__ == "__main__":
    # modtest.dotest()
    mcp.run(transport="stdio")
