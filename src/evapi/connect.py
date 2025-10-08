from dotenv import load_dotenv
import os
from wslib.WSClient import WSClient
from helper.mcplogger import logger

load_dotenv()


class EVConnect:
    EVAPI_URL = os.getenv("EVAPI_URL", "")
    EVAPI_USER = os.getenv("EVAPI_USER", "")
    EVAPI_PASS = os.getenv("EVAPI_PASS", "")

    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        if EVConnect.EVAPI_URL is None or EVConnect.EVAPI_URL == "":
            raise ValueError("No application URL")
        self.conn = WSClient(EVConnect.EVAPI_URL)
        if not self.conn.do_login(EVConnect.EVAPI_USER, EVConnect.EVAPI_PASS):
            raise ValueError(f"Login error: {EVConnect.EVAPI_USER}")
        logger.info("Connected to EVAPI at %s as %s", EVConnect.EVAPI_URL, EVConnect.EVAPI_USER)

    def get_connection(self):
        return self.conn

    def logout(self):
        if self.conn is not None:
            self.conn.logout()
            self.conn = None

    def is_connected(self):
        return self.conn is not None and self.conn.sessionid is not None
