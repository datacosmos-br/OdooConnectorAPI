"""odoo_utils.py Odoo utilities module for the OdooConnectorAPI FastAPI application."""
import os
import odoorpc  # type: ignore

# Configuração inicial do odoorpc via variáveis de ambiente
ODOO_HOST = os.getenv('ODOO_HOST', 'web')
ODOO_PORT = os.getenv('ODOO_PORT', '8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoodb')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')
ODOO_SSL = os.getenv('ODOO_SSL', 'false').lower() == 'true'  # Verifica se ODOO_SSL é 'true'

# Dependency function to obtain an instance of the Odoo client, to be used as a dependency in routes
# @asynccontextmanager
async def odoo_connection():
    """
    Retrieves an instance of the Odoo connection.

    Returns:
        The Odoo connection instance.

    Raises:
        Exception: If the Odoo service is temporarily unavailable.
    """
    protocol = 'jsonrpc+ssl' if ODOO_SSL else 'jsonrpc'
    odoo = None
    try:
        print(f"Attempting to connect to Odoo at {ODOO_HOST}:{ODOO_PORT} with SSL={ODOO_SSL}")
        odoo = odoorpc.ODOO(ODOO_HOST, protocol=protocol, port=int(ODOO_PORT))
        print(f"Attempting to login in Odoo with {ODOO_DB}:{ODOO_USERNAME}:********")
        odoo.login(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD)
        print("Connection with Odoo established successfully.")
        yield odoo
    finally:
        if odoo:
            odoo.logout()
