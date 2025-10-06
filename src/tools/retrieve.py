from mcp.server.fastmcp import FastMCP
from evapi.retrieve import Retrieve

def register(mcp: FastMCP):
    @mcp.tool()
    async def retrieve_record(wsid: str):
        """
        Retrieve the values of the fields available for a record in your Evolutivo Application.
        Args:
            wsid (str): The WSID of the record to retrieve.
        Returns:
            array: field values for the record identifier.
        """
        conn = Retrieve()
        return conn.get_entity(wsid)
