import os
from flask import send_file, jsonify

class RatesService:
    RATES_FILE_PATH = os.path.join(os.getcwd(), "in", "rates.xlsx")  # Save file in /in directory

    @staticmethod
    def process_rates_file(file):
        """
        Process and validate the uploaded rates file, and save it to a predefined location.

        :param file: The uploaded file object
        :return: Success message
        """
        try:
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(file)

            # Validate required columns
            required_columns = {"Product", "Rate", "Scope"}
            if not required_columns.issubset(df.columns):
                raise ValueError("The uploaded file must contain 'Product', 'Rate', and 'Scope' columns.")

            # Validate data types
            if not pd.api.types.is_numeric_dtype(df["Rate"]):
                raise ValueError("All 'Rate' values must be numeric.")

            # Save the file to the predefined /in directory
            os.makedirs(os.path.dirname(RatesService.RATES_FILE_PATH), exist_ok=True)
            file.save(RatesService.RATES_FILE_PATH)

            return {"message": "Rates file processed and saved successfully"}
        except ValueError as ve:
            raise ValueError(f"Validation error: {ve}")
        except Exception as e:
            raise IOError(f"Error processing the rates file: {e}")

    @staticmethod
    def get_rates_file_path():
        """
        Retrieve the path of the stored rates file.

        :return: File path if exists, None otherwise
        """
        if os.path.isfile(RatesService.RATES_FILE_PATH):
            return RatesService.RATES_FILE_PATH
        return None

    @staticmethod
    def download_rates_file():
        """
        Serve the stored rates file for download.

        :return: Flask response to download the file
        """
        file_path = RatesService.get_rates_file_path()
        if not file_path:
            raise FileNotFoundError("Rates file not found.")
        return send_file(file_path)

    @staticmethod
    def update_rate(rate_id, data):
        """
        Update a specific rate in the database.

        :param rate_id: ID of the rate to update
        :param data: Data containing the updated rate
        :return: The updated rate or None if not found
        """
        try:
            rate = RatesModel.query.get(rate_id)  # Replace with actual ORM logic
            if not rate:
                return None

            # Update rate details
            rate.Rate = data.get("Rate", rate.Rate)
            rate.save()  # Assuming save() commits changes to the DB

            return {"id": rate.id, "Product": rate.Product, "Rate": rate.Rate, "Scope": rate.Scope}
        except Exception as e:
            raise RuntimeError(f"Error updating rate: {e}")
