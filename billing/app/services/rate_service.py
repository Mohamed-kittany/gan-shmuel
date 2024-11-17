import os
import pandas as pd
from app.extensions import get_mysql_connection

class RateService:
    RATES_FILE_PATH = os.path.join(os.getcwd(), "in", "rates.xlsx")  # Save uploaded rates file

    @staticmethod
    def process_rates_file(file):
        """
        Process and save the uploaded rates file.

        :param file: Uploaded file object
        :return: Success message
        """
        try:
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(file)

            # Validate required columns
            required_columns = {"product_id", "rate", "scope"}
            if not required_columns.issubset(df.columns):
                raise ValueError("The uploaded file must contain 'product_id', 'rate', and 'scope' columns.")

            # Validate data types
            if not pd.api.types.is_numeric_dtype(df["rate"]):
                raise ValueError("All 'rate' values must be numeric.")

            # Save the file to the predefined directory
            os.makedirs(os.path.dirname(RateService.RATES_FILE_PATH), exist_ok=True)
            file.save(RateService.RATES_FILE_PATH)

            # Insert or update rows in the database
            connection = get_mysql_connection()
            cursor = connection.cursor()
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE rate = VALUES(rate), scope = VALUES(scope)",
                    (row["product_id"], row["rate"], row["scope"]),
                )
            connection.commit()
            connection.close()

            return {"message": "Rates file processed and saved successfully"}
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise IOError(f"Error processing the rates file: {e}")

    @staticmethod
    def get_all_rates():
        """Retrieve all rates from the database."""
        try:
            connection = get_mysql_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT r.product_id, r.rate, r.scope, p.name AS provider_name "
                "FROM Rates r LEFT JOIN Provider p ON r.scope = p.id"
            )
            rates = cursor.fetchall()
            connection.close()
            return rates
        except Exception as e:
            raise RuntimeError(f"Error fetching rates: {e}")

    @staticmethod
    def get_rate_by_product_id(product_id):
        """Retrieve a specific rate by product ID."""
        try:
            connection = get_mysql_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT r.product_id, r.rate, r.scope, p.name AS provider_name "
                "FROM Rates r LEFT JOIN Provider p ON r.scope = p.id WHERE r.product_id = %s",
                (product_id,),
            )
            rate = cursor.fetchone()
            connection.close()
            return rate
        except Exception as e:
            raise RuntimeError(f"Error fetching rate by product ID: {e}")

    @staticmethod
    def update_rate(product_id, data):
        """Update a specific rate in the database."""
        try:
            connection = get_mysql_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Rates SET rate = %s, scope = %s WHERE product_id = %s",
                (data["rate"], data["scope"], product_id),
            )
            connection.commit()
            cursor.execute("SELECT * FROM Rates WHERE product_id = %s", (product_id,))
            updated_rate = cursor.fetchone()
            connection.close()
            return updated_rate
        except Exception as e:
            raise RuntimeError(f"Error updating rate: {e}")

    @staticmethod
    def delete_rate(product_id):
        """Delete a specific rate by product ID."""
        try:
            connection = get_mysql_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Rates WHERE product_id = %s", (product_id,))
            connection.commit()
            connection.close()
            return cursor.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error deleting rate: {e}")
