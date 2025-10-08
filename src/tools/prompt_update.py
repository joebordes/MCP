from mcp.server.fastmcp import FastMCP
# from fastmcp.prompts import PromptMessage
# from mcp.types import TextContent

def register(mcp: FastMCP):

    @mcp.prompt()
    def update_procedure(wsid: str) -> list[str]:
        """
        Defines the steps to update a record.
        """
        return [
            f"Use get_entity_name_from_id in metainformation to obtain the entity name of the record {wsid}",
            f"Use get_fields metainformation to get a list of fields for the entity name obtained",
            f"Ask the user which fields to update",
            f"Loop over all the fields asking the user for values. Use the metainformation about field types to show possible values for each field",
            f"Validate each field with it's type",
            f"Use update tool to update the record",
            f"Inform the user about the result",
        ]

    @mcp.prompt()
    def quick_update_procedure(list_of_fields: dict, wsid: str) -> list[str]:
        """
        Defines the steps to update some fields of a record.
        """
        return [
            f"Update this {list_of_fields} in the record {wsid}",
            f"Use retrieve to show the user the current field values of the record",
            f"Use get_entity_name_from_id in metainformation to obtain the entity name of the record",
            f"Use the entity name and the get_fields metainformation tool to get the types of the fields to be updated",
            f"Loop over the list of fields and ask the user for the new values. Use the metainformation about field types to show possible values for each field",
            f"Validate each field with it's type",
            f"Use update tool to update the record",
            f"Inform the user about the result",
        ]

    @mcp.prompt()
    def update_field_procedure(field: str, wsid: str, value) -> list[str]:
        """
        Defines the steps to update a field in a record with a value.
        """
        return [
            f"Update {field} in the record {wsid} with the value {value}",
            f"Use retrieve to show the user the current field value of the record",
            f"Use get_entity_name_from_id in metainformation to obtain the entity name of the record",
            f"Use the entity name and the get_fields metainformation tool to get the type of the field to be updated",
            f"Validate the given value for the field with it's type",
            f"Use update tool to update the record",
            f"Inform the user about the result",
        ]
