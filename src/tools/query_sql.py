from mcp.server.fastmcp import FastMCP
from evapi.query import Query


def register(mcp: FastMCP):

    @mcp.tool()
    async def launch_query(
        select: str,
        object_name: str,
        where: str = None,
        order_by: str = None,
        limit: str = None
    ):
        """
        Launch an SQL-like query to your Evolutivo Application.

        Args:
            select (str): columns to select, e.g., '*', 'name,email', 'count(*)', 'sum(amount)'
            object_name (str): module/entity name
            where (str, optional): conditions e.g. "status='Active' and account_id in (1,2,3)"
            order_by (str, optional): columns to order by, max 2 columns
            limit (str, optional): either "n" or "m,n" for offset and limit

        Returns:
            array of array: results of the query
        """

        query = Query()
        vtql = query.get_query(
            select, object_name, where, order_by, limit
        )
        if vtql.startswith("Error:"):
            return "Query structure is invalid: " + vtql

        return query.get_records(vtql)
