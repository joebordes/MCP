from mcp.server.fastmcp import FastMCP
from evapi.create import Create

def register(mcp: FastMCP):
    @mcp.tool()
    async def create_record(entity: str, fields: dict):
        """
        Create a new record in the specified entity with the given fields in your Evolutivo Application.
        Args:
            entity (str): entity where the new record will be created
            fields (dict): dictionary with field names and their values for the new record
        Returns:
            string: entity identifier of the newly created record or an error message
        """
        conn = Create()
        return conn.do_create(entity, fields)
