from mcp.server.fastmcp import FastMCP
from evapi.metainformation import MetaInformation

mcp = FastMCP("EvolutivoFW MCP", "1.0.0")


@mcp.tool()
async def get_entities():
    """
    Retrieve the list of entities you can access from your Evolutivo Application.

    Returns:
        array of strings: List of entity names.
    """
    meta = MetaInformation()
    return meta.get_entities()

@mcp.tool()
async def get_fields(entity: str):
    """
    Retrieve the list of fields available for an entity in your Evolutivo Application.

    Returns:
        array of array: List of field information for the entity.
    """
    meta = MetaInformation()
    return meta.get_fields(entity)

@mcp.tool()
async def get_related_modules(entity: str):
    """
    Retrieve the list of entities related to an entity in your Evolutivo Application.

    Returns:
        array of strings: List of entity names related to the entity.
    """
    meta = MetaInformation()
    return meta.get_related_modules(entity)

if __name__ == "__main__":
    # modtest.dotest()
    mcp.run(transport="stdio")
