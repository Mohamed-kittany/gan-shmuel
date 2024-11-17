import logging
from app.extensions import get_mysql_connection

class TruckService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_truck(self, provider_id, truck_id):
        """
        Creates a new truck.
        Args:
            provider id (str): The id of the provider. Must be unique and must be in the system before.
            truck id (str): The truck id. Must be unique
        Returns:
            code 201
        Raises:
            ValueError: If the truck id already exists or if the provider id doesn't exist.
            Exception: For other database operation failures.
        """
        self.logger.info(f"Attempting to create truck with: {truck_id} and {provider_id}")
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            # Check if provider id exists
            cursor.execute("SELECT id FROM Provider WHERE id = %s", (provider_id,))
            if not cursor.fetchone():
                self.logger.warning(f"The provider id: '{provider_id}' does not exist")
                raise ValueError(f"There is no provider with the '{provider_id}' id")

            # Check if the truck id already exists
            cursor.execute("SELECT id FROM Trucks WHERE id = %s", (truck_id,))
            if cursor.fetchone():
                self.logger.warning(f"Truck id : '{truck_id}' already exists.")
                raise ValueError("A truck with this id already exists.")

            # Insert the truck into the database
            cursor.execute("INSERT INTO Trucks (id, provider_id) VALUES (%s, %s)", (truck_id, provider_id))
            connection.commit()
            self.logger.info(f"Truck '{truck_id}' was created successfully with the provider '{provider_id}'")
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Failed to create truck: {e}")
            raise
        finally:
            cursor.close()

        return 201

##############################################################to implamante
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
