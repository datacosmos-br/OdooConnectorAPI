"""Module to test connection to Odoo using odoorpc."""
import odoorpc # type: ignore


def test_odoo_connection():
    """Test connection to the Odoo server."""
    odoo = odoorpc.ODOO('localhost', port=8069)
    try:
        odoo.login('odoodb', 'admin', 'admin')  # Database, username, password
        print("Successfully connected to Odoo 17!")
    except ConnectionError as e:
        print(f"Error connecting to Odoo 17: {e}")


if __name__ == "__main__":
    test_odoo_connection()
