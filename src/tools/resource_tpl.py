from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FileResource
from evapi.retrieve import Retrieve
from helper.mcplogger import logger
import tempfile
import os
import mimetypes
import requests


def register(mcp: FastMCP):

    @mcp.resource("resource://{template}/{wsids}/{output_format}")
    def get_template_file_resource(template: str, wsids: str, output_format: str) -> FileResource:
        """
        Generate a data file from a document template saved in Evolutivo.FW and a list of records.
        Retrieve or get a PDF or ODT document generated from a template and one or more records.

        Args:
            template (str): id or name of template to generate document from
            wsids (str): comma-separated list of internal IDs to use as data source
            output_format (str): output format can be pdf, odt, onepdf, oneodt

        Returns:
            stream of bytes: contents of the generated document
        """
        try:
            conn = Retrieve()
            docinfo = conn.get_template_document(
                template, wsids, output_format)
            logger.info(docinfo)
            if docinfo is None or 'file' not in docinfo or not docinfo['file']:
                raise FileNotFoundError(
                    f"Document not generated for IDs: {wsids}")
            # Download the file from the URL to a temporary local file
            file_path = os.getenv("EVAPI_URL", "") + '/' + docinfo['file']
            response = requests.get(file_path, timeout=10)
            response.raise_for_status()  # Raise an error for bad status

            filename = os.path.basename(docinfo['file'])
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, filename)
            with open(temp_path, "wb") as f:
                f.write(response.content)

            if output_format in ['onepdf', 'oneodt'] or (
                output_format in ['pdf', 'odt'] and not docinfo["is_zip"]
            ):
                if output_format in ['onepdf', 'pdf']:
                    mimetype = "application/pdf"
                else:
                    mimetype = "application/vnd.oasis.opendocument.text"
            else:
                mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = "application/octet-stream"
            filesize = os.path.getsize(temp_path)

            metadata = {
                "filename": filename,
                "size": filesize,
                "mimetype": mimetype,
                "recordid": wsids,
            }

            logger.info("Decoded file: %s (%s, %d bytes)",
                        filename, mimetype, filesize)
            return FileResource(
                uri=f"resource://{wsids}/fromtemplate/{template}/format/{output_format}",
                name=filename,
                path=temp_path,
                mime_type=mimetype,
                metadata=metadata,
            )

        except Exception as e:
            logger.error("Error decoding API file: %s", e)
            raise

    @mcp.tool()
    def get_template_file(template: str, wsids: str, output_format: str) -> FileResource:
        """
        Generate a data file from a document template saved in Evolutivo.FW and a list of records.
        Retrieve or get a PDF or ODT document generated from a template and one or more records.

        Args:
            template (str): id or name of template to generate document from
            wsids (str): comma-separated list of internal IDs to use as data source
            output_format (str): output format can be pdf, odt, onepdf, oneodt

        Returns:
            stream of bytes: contents of the generated document
        """
        return get_template_file_resource(template, wsids, output_format)
