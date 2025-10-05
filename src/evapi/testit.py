from evapi.connect import EVConnect


def query(ws):
    try:
        result = ws.do_query("select * from helpdesk limit 2;")
        print(result)
    except (AttributeError, TypeError) as e:
        print(f"Error in query: {e}")

def list_types(ws):
    try:
        print(ws.do_listtypes)
    except (AttributeError, TypeError) as e:
        print(f"Error in list_types: {e}")

def dotest():
    try:
        evconn = EVConnect()
        ws = evconn.get_connection()
        print("Login OK")
        list_types(ws)
        query(ws)
        ws.logout()
    except (ConnectionError, AttributeError) as e:
        print(f"Error during login or main workflow: {e}")
    return "Test completed"
