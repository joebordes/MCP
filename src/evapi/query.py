from evapi.connect import EVConnect
from helper.mcplogger import logger
from evapi.metainformation import MetaInformation
import re

class Query:
    def __init__(self):
        self.evconn = EVConnect()
        self.ws = self.evconn.get_connection()

    def get_query(
        self,
        select: str,
        object_name: str,
        where: str = None,
        order_by: str = None,
        limit: str = None
    ):
        try:
            # Validate select
            select = select.strip()
            if not select:
                logger.error("Error: 'select' cannot be empty")
                return "Error: 'select' cannot be empty"

            # Validate object_name
            object_name = object_name.strip()
            if not object_name:
                logger.error("Error: 'object_name' cannot be empty")
                return "Error: 'object_name' cannot be empty"

            query = f"SELECT {select} FROM {object_name}"

            # Add WHERE clause
            if where:
                where = where.strip()
                if where:
                    query += f" WHERE {where}"

            # Add ORDER BY clause
            if order_by:
                order_by_cols = [col.strip() for col in order_by.split(",")]
                if len(order_by_cols) > 2:
                    logger.error("Error: ORDER BY can have at most two columns")
                    return "Error: ORDER BY can have at most two columns"
                query += f" ORDER BY {', '.join(order_by_cols)}"

            # Add LIMIT clause
            if limit:
                limit = limit.strip()
                # normalize m,n or n
                if "," in limit:
                    m, n = [x.strip() for x in limit.split(",")]
                    query += f" LIMIT {m}, {n}"
                else:
                    query += f" LIMIT {limit}"

            # Ensure semicolon at the end
            query = query.rstrip(";") + ";"

            return query
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in construct query: %s", e)
            return []

    def parse_query(self, command: str):
        command = command.strip()
        if not command:
            return "Error: command cannot be empty"

        # Lowercase for parsing keywords but preserve original for column names
        cmd_lower = command.lower()

        # --- FROM (object/entity) ---
        from_match = re.search(r"from\s+(\w+)", command, re.IGNORECASE)
        if from_match:
            object_name = from_match.group(1).strip()
        else:
            # fallback for "Get all Contacts ..."
            fallback = re.search(r"get all (\w+)", command, re.IGNORECASE)
            if fallback:
                object_name = fallback.group(1).strip()
            else:
                return "Error: could not detect object/entity"

        # Define trigger phrases for "get all" style commands
        select_triggers = ["get", "list", "show"]
        select_all_triggers = ["get all", "list all", "show all"]
        # --- SELECT ---
        select_match = re.search(r"select\s+(.*?)\s+from", command, re.IGNORECASE)
        if select_match:
            select_clause = select_match.group(1).strip()
        elif any(trigger in cmd_lower for trigger in select_all_triggers):
            select_clause = "*"
        elif any(trigger in cmd_lower for trigger in select_triggers):
            meta = MetaInformation()
            select_clause = ','.join(meta.get_filter_fields(object_name))
        else:
            return "Error: could not detect SELECT clause"

        query = f"SELECT {select_clause} FROM {object_name}"

        # --- WHERE ---
        where_match = re.search(r"where\s+(.*?)(order by|limit|$)", command, re.IGNORECASE)
        if where_match:
            where_clause = where_match.group(1).strip()
            # Replace simple "is" with "="
            where_clause = re.sub(r"\s+is\s+", " = ", where_clause, flags=re.IGNORECASE)
            # Replace comma-separated values in IN
            where_clause = re.sub(r"in\s+([0-9, ]+)", lambda m: f"in ({m.group(1)})", where_clause, flags=re.IGNORECASE)
            logger.info("Where clause detected: %s", where_clause)
            query += f" WHERE {where_clause}"

        # --- ORDER BY ---
        # Capture up to (but not including) a trailing 'limit', 'where', ';' or end-of-string.
        order_match = re.search(
            r"order\s+by\s+([A-Za-z0-9_\.]+(?:\s*,\s*[A-Za-z0-9_\.]+)*)\s*(?=(?:limit\b|where\b|;|$))",
            command,
            re.IGNORECASE,
        )
        if order_match:
            cols = [c.strip() for c in order_match.group(1).split(",")][:2]  # max 2 columns
            logger.info("Order by columns detected: %s", ", ".join(cols))
            query += f" ORDER BY {', '.join(cols)}"

        # --- LIMIT ---
        limit_match = re.search(r"limit\s+([0-9, ]+)", command, re.IGNORECASE)
        if limit_match:
            limit_clause = limit_match.group(1).strip()
            logger.info("Limit clause detected: %s", limit_clause)
            # Normalize m,n or n
            if "," in limit_clause:
                m, n = [x.strip() for x in limit_clause.split(",")]
                query += f" LIMIT {m}, {n}"
            else:
                query += f" LIMIT {limit_clause}"

        # End with semicolon
        return query.rstrip(";") + ";"

    def get_records(self, query: str):
        try:
            logger.info("Executing query: %s", query)
            recs = self.ws.do_query(query)
            return recs
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error in get records for %s: %s", query, e)
            return []
