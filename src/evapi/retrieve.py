from evapi.connect import EVConnect
from helper.mcplogger import logger


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
