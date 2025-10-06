from mcp.server.fastmcp import FastMCP
from evapi.delete import Delete

def register(mcp: FastMCP):
    @mcp.tool()
    async def delete_record(wsid: str):
        """
        Delete a record from an entity in your Evolutivo Application.
        Args:
            wsid (str): The WSID of the record to delete.
        Returns:
            array: succes or error message.
        """
        conn = Delete()
        return conn.do_delete(wsid)
