from flask import Blueprint, jsonify
import logging
from ..services import BillService

billing_bp = Blueprint('bill', __name__)

logger = logging.getLogger(__name__)

WEIGHT_SERVICE_URL = "http://weight-app:6000"

@billing_bp.route("/bill/<id>?from=t1&to=t2", methods=["GET"])
def make_bill(id, time_start, time_end):
    
    """
    this function will make and return a bill

    Expects : id (provider id), time to start, time to end
    Return: Returns a json:
    {
    "id": <str>,
    "name": <str>,
    "from": <str>,
    "to": <str>,
    "truckCount": <int>,
    "sessionCount": <int>,
    "products": [
        { "product":<str>,
        "count": <str>, // number of sessions
        "amount": <int>, // total kg
        "rate": <int>, // agorot
        "pay": <int> // agorot
        },
        ...
        ...
        ...
    ],
    "total": <int> // agorot
    }
    """
    
    logger.info("Received request to create a Bill.")


