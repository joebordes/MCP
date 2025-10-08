from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FileResource
from evapi.retrieve import Retrieve
from helper.mcplogger import logger
import base64
import tempfile
import io
import os


def register(mcp: FastMCP):

    @mcp.resource("resource://{wsid}")
    def get_file_resource(wsid: str) -> FileResource:
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
            # Save to a temporary file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, filename)
            with open(temp_path, "wb") as f:
                f.write(io.BytesIO(base64.b64decode(attachment_b64)).read())

            logger.info("Decoded file: %s (%s, %d bytes)", filename, mimetype, filesize)
            return FileResource(
                uri=f"resource://{wsid}",
                name=filename,
                path=temp_path,
                mime_type=mimetype,
                metadata=metadata,
            )

        except Exception as e:
            logger.error("Error decoding API file: %s", e)
            raise

    @mcp.tool()
    def get_file(wsid: str) -> FileResource:
        """
        Retrieve data from a document saved in Evolutivo.FW.

        Args:
            wsid (str): internal ID of the document (e.g., '12x34567')

        Returns:
            stream of bytes: contents of the document
        """
        return get_file_resource(wsid)
