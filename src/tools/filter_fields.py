from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

def register(mcp: FastMCP):
    @mcp.tool()
    async def get_filter_fields(entity: str):
        """
        Retrieve the list of filter fields available for an entity in your Evolutivo Application.
        Returns:
            array of array: List of field names for the entity.
        """
        meta = MetaInformation()
        return meta.get_filter_fields(entity)
