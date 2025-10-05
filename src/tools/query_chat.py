from mcp.server.fastmcp import FastMCP
from evapi.query import Query

def register(mcp: FastMCP):

    @mcp.tool()
    async def launch_query_from_text(command: str):
        """
        Parse a free-text command and create an SQL-like query for your Evolutivo Application.

        Example commands:
        - "Get all Contacts where status is Active and account_id in 1,2,3 order by name,email limit 10"
        - "Select name,email from Contacts where name like 'Joe%' limit 5"

        Args:
            command (str): free-text SQL-like request from user

        Returns:
            array of array: results of the query
        """
        query = Query()
        vtql = query.parse_query(command)
        if vtql.startswith("Error:"):
            return "Error: query structure is invalid: " + vtql

        return query.get_records(vtql)
