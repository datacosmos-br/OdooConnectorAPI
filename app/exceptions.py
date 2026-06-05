"""QueryFormatError module for the OdooConnectorAPI FastAPI application."""
class QueryFormatError(Exception):
    """Exception for errors in the query format."""
    def __init__(self, message: str = "Query format is invalid"):
        self.message = message
        super().__init__(self.message)
