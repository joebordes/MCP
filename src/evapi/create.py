from evapi.connect import EVConnect
from helper.mcplogger import logger


class Create:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def do_create(self, entity: str, fields: dict):
        try:
            record = self.ws.do_create(entity, fields)
            return record
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in create entity (%s): %s", entity, e)
            return []
