from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

def register(mcp: FastMCP):
    @mcp.tool()
    async def get_related_modules(entity: str):
        """
        Retrieve the list of entities related to an entity in your Evolutivo Application.
        Returns:
            array of strings: List of entity names related to the entity.
        """
        meta = MetaInformation()
        return meta.get_related_modules(entity)
