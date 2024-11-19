import logging
from app.extensions import get_mysql_connection

class BillService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    

    
    def get_unique_trucks(provider_id:int):
        """
        Returns a list of unique truck ids.
        """
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM TRUCKS WHERE provider_id = %s", (provider_id,))
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def initialize_product_entry(product_name):
        
        return {
            "product": product_name,
            "count": 0,     # Number of sessions
            "amount": 0,    # Total kg
            "rate": 0,      # Agorot
            "pay": 0        # Agorot
        }
    
    def get_rates_by_product(prodcut_id:str):
        """
        Returns the rate for a given product.
        """
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT rate FROM RATES WHERE product_id = %s", (prodcut_id,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
