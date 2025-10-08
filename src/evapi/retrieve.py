from evapi.connect import EVConnect
from helper.mcplogger import logger
import urllib.parse
import json


class Retrieve:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def get_entity(self, wsid: str):
        try:
            record = self.ws.do_retrieve(wsid)
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get entity (%s): %s", wsid, e)
            return []

    def get_document(self, wsid: str):
        try:
            record = self.ws.do_invoke('retrievedocattachment', {'id': wsid, 'returnfile': True})
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get document for %s: %s", wsid, e)
            return None

    def get_template_document(self, template: str, wsids: str, output_format: str = 'pdf'):
        try:
            decoded_template = urllib.parse.unquote(template)
            ids_list = wsids.split(",")
            if len(ids_list) == 1:
                if output_format == 'pdf':
                    output_format = 'onepdf'
                elif output_format == 'odt':
                    output_format = 'oneodt'
            record = self.ws.do_invoke(
                'getmergedtemplate',
                {
                    "template": decoded_template,
                    "crmids": json.dumps(ids_list),
                    "output_format": output_format
                },
                "GET"
            )
            file_path = record.get("file", "")
            cache_index = file_path.find("cache/gendocoutput")
            if cache_index != -1:
                record["file"] = file_path[cache_index:]
            record["is_zip"] = len(ids_list) > 1
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get template document for %s %s %s: %s",
                         decoded_template, wsids, output_format, e)
            return None
