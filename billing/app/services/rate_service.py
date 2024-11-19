import os
import pandas as pd
from openpyxl import load_workbook
from app.extensions import get_mysql_connection
from pyexcel_ods import get_data as read_ods


class RateService:
    RATES_FILE_PATH = os.path.join(os.getcwd(), "in", "rates.xlsx")  # Path to save the uploaded rates file

    @staticmethod
    def process_and_save_rates(filepath):
        try:
            # Convert to DataFrame based on file type
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.ods'):
                data = read_ods(filepath)  # Replace with parse_ods if using `odfpy`
                sheet_name = next(iter(data))
                df = pd.DataFrame(data[sheet_name][1:], columns=data[sheet_name][0])
            else:  # Assume it's an Excel file
                df = pd.read_excel(filepath, engine='openpyxl')

            # Validate required columns
            required_columns = {"Product", "Rate", "Scope"}
            if not required_columns.issubset(df.columns):
                raise ValueError("The uploaded file must contain 'Product', 'Rate', and 'Scope' columns.")

            # Normalize and validate "Scope" column
            df["Scope"] = df["Scope"].astype(str).str.upper().str.strip()

            # Validate data types
            if not pd.api.types.is_numeric_dtype(df["Rate"]):
                raise ValueError("All 'Rate' values must be numeric.")

            # Convert rates to integers
            df["Rate"] = df["Rate"].astype(int)

            # Check for missing values in required columns
            if df[["Product", "Rate", "Scope"]].isnull().any().any():
                raise ValueError("The file contains missing values in required columns (Product, Rate, or Scope).")

            # Save rates to the database with precedence logic
            connection = get_mysql_connection()
            cursor = connection.cursor()

            # Clear existing rates to overwrite
            cursor.execute("DELETE FROM Rates")

            # Process and insert new rates
            for product, group in df.groupby("Product"):
                # Sort group to prioritize scoped rates over "ALL"
                group = group.sort_values(by="Scope", key=lambda x: x != "ALL")  # Scoped rates come first

                for _, row in group.iterrows():
                    product_id = row["Product"]
                    rate = row["Rate"]
                    scope = row["Scope"]

                    # Insert the rate into the database
                    cursor.execute(
                        """
                        INSERT INTO Rates (product_id, rate, scope)
                        VALUES (%s, %s, %s)
                        """,
                        (product_id, rate, scope)
                    )

            connection.commit()
            connection.close()

            # Save the new rates file as "rates.xlsx", replacing the old one
            os.makedirs(os.path.dirname(RateService.RATES_FILE_PATH), exist_ok=True)
            df.to_excel(RateService.RATES_FILE_PATH, index=False)

            # Remove the uploaded file if it has a different name
            if filepath != RateService.RATES_FILE_PATH:
                os.remove(filepath)

            return {"message": "Rates file processed and saved successfully"}

        except ValueError as ve:
            raise ValueError(f"Validation error: {ve}")
        except Exception as e:
            raise Exception(f"Error processing the rates file: {e}")



    @staticmethod
    def get_all_rates():
        """Retrieve all rates from the database."""
        try:
            connection = get_mysql_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM Rates")
            rates = cursor.fetchall()
            connection.close()

            return rates
        except Exception as e:
            raise RuntimeError(f"Error fetching rates: {e}")
