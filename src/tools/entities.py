from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

def register(mcp: FastMCP):
    @mcp.tool()
    async def get_entities():
        """
        Retrieve the list of entities you can access from your Evolutivo Application.
        Returns:
            array of strings: List of entity names.
        """
        meta = MetaInformation()
        return meta.get_entities()
