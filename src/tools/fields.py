from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

def register(mcp: FastMCP):
    @mcp.tool()
    async def get_fields(entity: str):
        """
        Retrieve the list of fields available for an entity in your Evolutivo Application.
        Returns:
            array of array: List of field information for the entity.
        """
        meta = MetaInformation()
        return meta.get_fields(entity)
