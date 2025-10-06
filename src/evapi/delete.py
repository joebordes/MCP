from evapi.connect import EVConnect
from helper.mcplogger import logger


class Delete:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def do_delete(self, wsid: str):
        try:
            record = self.ws.do_delete(wsid)
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get entity (%s): %s", wsid, e)
            return []
