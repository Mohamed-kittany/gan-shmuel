import os
import pandas as pd
from flask import send_file
from ..models import RatesModel  # Replace with your ORM-based model

class RatesService:
    RATES_FILE_PATH = "/in/rates.xlsx"  # Path inside the container

    @staticmethod
    def process_rates_file(file):
        """
        Process and save the uploaded rates file.

        :param file: The uploaded file object
        :return: Success message
        """
        try:
            # Read the file content (Excel file)
            df = pd.read_excel(file)

            # Validate required columns
            required_columns = {"Product", "Rate", "Scope"}
            if not required_columns.issubset(df.columns):
                raise ValueError("The uploaded file must contain 'Product', 'Rate', and 'Scope' columns.")

            # Validate data types
            if not all(isinstance(rate, (int, float)) for rate in df["Rate"]):
                raise ValueError("All rates must be numeric.")

            # Save the file to the predefined /in directory
            os.makedirs(os.path.dirname(RatesService.RATES_FILE_PATH), exist_ok=True)
            file.save(RatesService.RATES_FILE_PATH)
            return {"message": "Rates file processed and saved successfully"}
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise IOError(f"Failed to save rates file: {e}")

    @staticmethod
    def get_rates_file_path():
        """
        Get the path of the stored rates file.

        :return: File path if exists, None otherwise
        """
        if os.path.isfile(RatesService.RATES_FILE_PATH):
            return RatesService.RATES_FILE_PATH
        return None

    @staticmethod
    def download_rates_file(file_path):
        """
        Serve the stored rates file for download.

        :param file_path: Path to the rates file
        :return: Flask response to download the file
        """
        return send_file(file_path)

    @staticmethod
    def update_rate(rate_id, data):
        """
        Update a specific rate in the database.

        :param rate_id: ID of the rate to update
        :param data: Data containing the updated rate
        :return: The updated rate or None if not found
        """
        # Simulate database access (replace with actual DB logic)
        rate = RatesModel.get_by_id(rate_id)  # Assuming a RatesModel exists
        if not rate:
            return None

        rate.Rate = data["Rate"]
        rate.save()  # Assuming save() commits changes to the DB
        return {"id": rate.id, "Product": rate.Product, "Rate": rate.Rate, "Scope": rate.Scope}
