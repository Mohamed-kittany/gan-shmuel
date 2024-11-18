import logging
from flask import Blueprint, jsonify, request # type: ignore
from ..services import ProviderService

provider_bp = Blueprint('provider', __name__)
provider_service = ProviderService()

logger = logging.getLogger(__name__)

@provider_bp.route('/provider', methods=['POST'])
def create_provider():
    """
    Creates a new provider record.
    Expects JSON payload: { "name": <str> }
    Returns: { "id": <str> }
    """
    logger.info("Received request to create a provider.")
    data = request.get_json()
    name = data.get("name")
    if not name:
        logger.error("Provider name is missing in the request.")
        return jsonify({"error": "Provider name is required"}), 400

    try:
        provider_id = provider_service.create_provider(name)
        logger.info(f"Provider created successfully with ID: {provider_id}")
        return jsonify({"id": str(provider_id)}), 201
    except ValueError as ve:
        logger.warning(f"Failed to create provider: {ve}")
        return jsonify({"error": str(ve)}), 409
    except Exception as e:
        logger.error(f"Error creating provider: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@provider_bp.route('/provider/<int:provider_id>', methods=['PUT'])
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
