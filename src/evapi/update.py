from evapi.connect import EVConnect
from helper.mcplogger import logger


class Update:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def do_update(self, fields: dict):
        try:
            record = self.ws.do_revise(fields)
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in update entity (%r): %s", fields, e)
            return []
