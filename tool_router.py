from browser import google_search
from browser import open_website

def run_tool(action):

    if not isinstance(action, dict):
        print("Invalid action (expected dict)")
        return

    tool = action.get("tool")
    if not tool:
        print("Invalid action (missing 'tool')")
        return

    if tool == "open_website":
        url = action.get("url")
        if not url:
            print("Invalid action for open_website (missing 'url')")
            return
        open_website(url)
    
    elif tool == "google_search":
        query = action.get("query")
        if not query:
            print("Invalid action for google_search (missing 'query')")
            return
        google_search(query)

    else:
        print("Tool not found")           