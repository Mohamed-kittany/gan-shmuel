import logging
from flask import Blueprint, jsonify, request
from ..services import TruckService

truck_bp = Blueprint('truck', __name__)
truck_service = TruckService()

logger = logging.getLogger(__name__)

@truck_bp.route('/truck', methods=['POST'])
def create_truck():
    """
    registers a truck in the system
    - provider - known provider id
    - id - the truck license plate
    """
    logger.info("Received request to create a new truck.")
    data = request.get_json()
    provider_id = data.get("provider_id")
    truck_id = data.get("id")

    if not truck_id:
        logger.error("Truck id is missing in the request.")
        return jsonify({"error": "Truck id is required"}), 400
    
    if not provider_id:
        logger.error("Provider id is missing in the request.")
        return jsonify({"error": "Provider id is required"}), 400
    
    try:
        truck_service.create_truck(provider_id, truck_id)
        logger.info(f"Truck created successfully")
        return 201 #need to hcnage it makes a problem with http
    except ValueError as ve:
        logger.warning(f"Failed to create Truck: {ve}")
        return jsonify({"error": str(ve)}), 409
    except Exception as e:
        logger.error(f"Error creating Truck: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

#####################################################to implamante
@truck_bp.route('/provider/<int:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    """
    Updates the name of an existing provider.
    Expects JSON payload: { "name": <str> }
    """
    logger.info(f"Received request to update provider with ID: {provider_id}")
    data = request.get_json()
    name = data.get("name")
    
    if not name:
        logger.error("Provider name is missing in the request.")
        return jsonify({"error": "Provider name is required"}), 400

    try:
        provider_service.update_provider(provider_id, name)
        logger.info(f"Provider with ID: {provider_id} updated successfully to name: {name}.")
        return jsonify({"message": "Provider updated successfully"}), 200
    except ValueError as ve:
        logger.warning(f"Failed to update provider: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        if "already exists" in str(e):
            logger.warning(f"Attempt to use duplicate name for Provider ID: {provider_id}: {e}")
            return jsonify({"error": "A provider with this name already exists."}), 409
        logger.error(f"Error updating provider with ID: {provider_id}: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
