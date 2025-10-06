from mcp.server.fastmcp import FastMCP
from evapi.retrieve import Retrieve
from helper.mcplogger import logger
import json


def register(mcp: FastMCP):

    @mcp.tool()
    def get_data(wsid: str) -> str:
        """
        Retrieve data from a document saved in Evolutivo.FW.

        Args:
            wsid (str): internal ID of the document (e.g., '12x34567')

        Returns:
            stream of bytes: contents of the document
        """
        try:
            conn = Retrieve()
            docinfo = conn.get_document(wsid)
            if docinfo is None:
                raise FileNotFoundError(f"Document not found for ID: {wsid}")

            file_info = docinfo[wsid]
            attachment_b64 = file_info.get("attachment")
            if not attachment_b64:
                raise ValueError("Missing 'attachment' field")

            filename = file_info.get("filename", "unknown.bin")
            mimetype = file_info.get("filetype", "application/octet-stream")
            filesize = file_info.get("filesize", 0)

            metadata = {
                "filename": filename,
                "size": filesize,
                "mimetype": mimetype,
                "recordid": wsid,
            }

            logger.info("Decoded file: %s (%s, %d bytes)", filename, mimetype, filesize)
            return json.dumps({
                "name": filename,
                "mime_type": mimetype,
                "data": attachment_b64,
                "metadata": metadata,
            })

        except Exception as e:
            logger.error("Error decoding API file: %s", e)
            raise


