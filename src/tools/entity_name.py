from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

def register(mcp: FastMCP):
    @mcp.tool()
    async def get_entity_name_from_id(wsid: str) -> str:
        """
        Retrieve the entity name of a record ID in your Evolutivo Application.
        Returns:
            string: entity name.
        """
        meta = MetaInformation()
        return meta.get_entity_name_from_id(wsid)
