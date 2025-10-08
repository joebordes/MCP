from mcp.server.fastmcp import FastMCP
from evapi.update import Update

def register(mcp: FastMCP):
    @mcp.tool()
    async def update_record(fields: dict):
        """
        Update an existing record with the given fields in your Evolutivo Application.
        Args:
            fields (dict): dictionary with field names and their new values. One field MUST be the ID of the existing record
        Returns:
            array: field values of the updated record.
        """
        conn = Update()
        return conn.do_update(fields)
