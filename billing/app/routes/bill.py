from flask import Blueprint, jsonify
import logging
from ..services import BillService

billing_bp = Blueprint('bill', __name__)

logger = logging.getLogger(__name__)

@billing_bp.route("/bill/<id>?from=t1&to=t2", methods=["GET"])
def get_bill(id, time_start, time_end):
    logger.info("Received request to create a Bill.")
    
