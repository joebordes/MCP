from evapi.connect import EVConnect
from helper.mcplogger import logger


class MetaInformation:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def get_entities(self):
        try:
            tables = self.ws.do_listtypes
            return tables["types"]
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get entities: %s", e)
            return []

    def get_entity_name_from_id(self, wsid: str) -> str:
        try:
            info = self.ws.do_invoke('getEntityNameFromID', {"entityid":wsid}, "GET")
            return info
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get entity name from id %s: %s", wsid, e)
            return ''

    def get_fields(self, entity):
        try:
            info = self.ws.do_describe(entity)
            fields = info.get("fields", [])

            # List of keys we want to keep
            keys_to_keep = [
                "name",
                "label",
                "mandatory",
                "type",
                "editable",
                "helpinfo",
                "sequence",
                "block",
                "displaytype",
                "default"
            ]

            # Filter each field to keep only the selected keys
            filtered_fields = [
                {k: f.get(k) for k in keys_to_keep if k in f}
                for f in fields
            ]

            return filtered_fields
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get fields for %s: %s", entity, e)
            return []

    def get_related_modules(self, entity):
        try:
            info = self.ws.do_describe(entity)
            return list(info["relatedModules"].keys())
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get related modules for %s: %s", entity, e)
            return []

    def get_filter_fields(self, entity):
        try:
            info = self.ws.do_invoke('getfilterfields', {"module":entity})
            return list(info["fields"])
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get filter fields for %s: %s", entity, e)
            return []
