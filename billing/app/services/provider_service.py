import logging
from app.extensions import get_mysql_connection

class ProviderService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_provider(self, name):
        """
        Creates a new provider.
        Args:
            name (str): The name of the provider. Must be unique.
        Returns:
            int: The ID of the newly created provider.
        Raises:
            ValueError: If the provider name already exists.
            Exception: For other database operation failures.
        """
        self.logger.info(f"Attempting to create provider with name: {name}")
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            # Check if the provider name already exists
            cursor.execute("SELECT id FROM Provider WHERE name = %s", (name,))
            if cursor.fetchone():
                self.logger.warning(f"Provider with name '{name}' already exists.")
                raise ValueError("A provider with this name already exists.")

            # Insert the provider record
            cursor.execute("INSERT INTO Provider (name) VALUES (%s)", (name,))
            connection.commit()
            provider_id = cursor.lastrowid
            self.logger.info(f"Provider created successfully with ID: {provider_id}")
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Failed to create provider: {e}")
            raise
        finally:
            cursor.close()

        return provider_id

    def update_provider(self, provider_id, name):
        """
        Updates the name of an existing provider.
        Args:
            provider_id (int): The ID of the provider to update.
            name (str): The new name for the provider.
        Raises:
            ValueError: If the provider does not exist or if the name already exists.
            Exception: For database operation failures.
        """
        self.logger.info(f"Attempting to update provider ID: {provider_id} with name: {name}")
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            # Check if provider exists
            cursor.execute("SELECT id FROM Provider WHERE id = %s", (provider_id,))
            if not cursor.fetchone():
                self.logger.warning(f"Provider ID: {provider_id} not found.")
                raise ValueError("Provider not found.")

            # Check if the new name already exists
            cursor.execute("SELECT id FROM Provider WHERE name = %s AND id != %s", (name, provider_id))
            if cursor.fetchone():
                self.logger.warning(f"Provider name '{name}' already exists for another provider.")
                raise ValueError("A provider with this name already exists.")

            # Update the provider name
            cursor.execute(
                "UPDATE Provider SET name = %s WHERE id = %s",
                (name, provider_id)
            )
            connection.commit()
            self.logger.info(f"Provider ID: {provider_id} updated successfully to name: {name}")
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Unexpected error while updating provider ID: {provider_id} - {e}")
            raise
        finally:
            cursor.close()
