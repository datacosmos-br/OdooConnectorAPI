"""Utilities module for the OdooConnectorAPI FastAPI application."""
from typing import Any, Dict

def error_response(error: Exception, msg: str) -> Dict[str, Any]:
    """
    Generates an error response dictionary.

    Args:
        error (Exception): The exception object.
        msg (str): The error message.

    Returns:
        dict: The error response dictionary.
    """
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }
