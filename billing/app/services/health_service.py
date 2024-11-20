import logging
from app.extensions import get_mysql_connection

class HealthService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def perform_health_check(self):
        """
        Checks the health of the application, including the database connection.
        Returns a tuple with the health status and HTTP status code.
        """
        try:
            conn = get_mysql_connection()
            conn.cursor().execute("SELECT 1")
            self.logger.info("Health check passed: Database connection successful.")
            return {"status": "OK :)!"}, 200
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {"status": "Failure"}, 500
