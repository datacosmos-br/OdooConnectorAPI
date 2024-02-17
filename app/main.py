"""Main module for the OdooConnectorAPI FastAPI application."""
import os
from typing import Dict, Any
from fastapi import FastAPI
import odoorpc # type: ignore

app = FastAPI()

# Configuração inicial do odoorpc via variáveis de ambiente
ODOO_URL = os.getenv('ODOO_URL', 'localhost')
ODOO_DB = os.getenv('ODOO_DB', 'mydb')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')


@app.get("/")
async def root():
    """Root GET endpoint returning a welcome message."""
    return {"message": "Hello World"}


@app.get("/get/partners")
async def get_partners() -> Dict[str, Any]:
    """GET endpoint to fetch partners from Odoo."""
    try:
        odoo = odoorpc.ODOO(ODOO_URL, port=80)
        odoo.login(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD)
    except odoorpc.error.RPCError as err:
        return {"error": err}

    partner = None
    partners = []  # Initialize the partners variable with an empty list
    if odoo.env:
        partner = odoo.env['res.partner']
        partners = partner.read(partner.search([]), ['name', 'email'])
    odoo.logout()
    return {"partners": partners}
