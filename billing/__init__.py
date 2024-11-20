
# /billing/app/tests/__init__.py
import pytest # type: ignore
from app import create_app
from app.extensions import get_mysql_connection
import pandas as pd
import io

def reset_test_database():
    """
    Resets the test database by truncating and re-inserting initial mock data.
    """
    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Reset the database tables
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE Rates;")
    cursor.execute("TRUNCATE TABLE Trucks;")
    cursor.execute("TRUNCATE TABLE Provider;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()

    # Re-insert mock data
    cursor.execute("INSERT INTO Provider (id, name) VALUES (1, 'ALL'), (2, 'pro1'), (3, 'pro2'), (4, 'Duplicate Name');")
    cursor.execute("INSERT INTO Rates (product_id, rate, scope) VALUES ('prod1', 10, 1), ('prod2', 20, 2), ('prod3', 30, 3);")
    cursor.execute("INSERT INTO Trucks (id, provider_id) VALUES ('T-001', 1), ('T-002', 2), ('T-003', 3);")
    conn.commit()

    conn.close()



@pytest.fixture
def mock_excel_file():
    """Create a mock Excel file with valid data."""
    def create_excel():
        data = {
            "product_id": ["prod4", "prod5"],
            "rate": [50, 60],
            "scope": [1, 2]
        }
        buffer = io.BytesIO()
        pd.DataFrame(data).to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    yield create_excel()  # Yield the file for use


@pytest.fixture
def mock_excel_file_invalid_columns():
    """Create a mock Excel file with missing columns."""
    def create_invalid_columns_excel():
        data = {
            "product_id": ["prod6"],
            "rate": [70]
        }
        buffer = io.BytesIO()
        pd.DataFrame(data).to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    yield create_invalid_columns_excel()  # Yield the file for use


@pytest.fixture
def mock_excel_file_invalid_data():
    """Create a mock Excel file with invalid data types."""
    def create_invalid_data_excel():
        data = {
            "product_id": ["prod7"],
            "rate": ["not_a_number"],
            "scope": [3]
        }
        buffer = io.BytesIO()
        pd.DataFrame(data).to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer
    
    yield create_invalid_data_excel()  # Yield the file for use


@pytest.fixture
def client():
    """
    Flask test client fixture with database rollback.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["MYSQL_DATABASE_DB"]="billdb_test"
    
    with app.test_client() as client:
        yield client

    # Cleanup: Reset database after the test
    reset_test_database()

