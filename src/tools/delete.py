from mcp.server.fastmcp import FastMCP
from evapi.delete import Delete

def register(mcp: FastMCP):
    @mcp.tool()
    async def delete_record(wsid: str):
        """
        Retrieve the values of the fields available for a record in your Evolutivo Application.
        Args:
            wsid (str): The WSID of the record to retrieve.
        Returns:
            array: field values for the record identifier.
        """
        conn = Delete()
        return conn.do_delete(wsid)
