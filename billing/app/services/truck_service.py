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
            # Check if provider id exists if it is go on
            cursor.execute("SELECT id FROM Provider WHERE id = %s", (provider_id,))
            if not cursor.fetchone():
                self.logger.warning(f"The provider id: '{provider_id}' does not exist")
                raise ValueError(f"There is no provider with the '{provider_id}' id")

            # Check if the truck id already exists if it isnt go on
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


    def update_truck(self, id, provider_id):
        """
        Updates the provider id of an existing truck.
        Args:
            id (str): the ID of an existing truck
            provider_id (int): The ID of the provider.
        Raises:
            ValueError: If the id does not exist or if the provider id dosnt exist in providers table.
            Exception: For database operation failures.
        """
        self.logger.info(f"Attempting to update tuck ID: {id} with provider id: {provider_id}")
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            #check if provider id exists go on
            cursor.execute("SELECT id FROM Provider WHERE id = %s", (provider_id,))
            if not cursor.fetchone():
                self.logger.warning(f"The provider id: '{provider_id}' does not exist")
                raise ValueError(f"There is no provider with the '{provider_id}' id")

            # Check if id exists if it is go on
            cursor.execute("SELECT id FROM Trucks WHERE id = %s", (id,))
            if not cursor.fetchone():
                self.logger.warning(f"Trcuk with ID: '{id}' dose not exists.")
                raise ValueError("A truck with this id dosnt exists.")

            # Update the provider name
            cursor.execute(
                "UPDATE Trucks SET provider_id = %s WHERE id = %s",
                (provider_id, id)
            )
            connection.commit()
            self.logger.info(f"Truck ID number: {id} updated successfully to provider ID: {provider_id}")
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Unexpected error while updating provider ID: {provider_id} - {e}")
            raise
        finally:
            cursor.close()
