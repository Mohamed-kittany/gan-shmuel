from flask import Blueprint, jsonify, request
import logging
from ..services import BillService
import os

WEIGHT_SERVICE_URL = f'http://{os.getenv("WEIGHT_SERVICE_HOST")}:{os.getenv("WEIGHT_SERVICE_PORT")}'


billing_bp = Blueprint('bill', __name__)

logger = logging.getLogger(__name__)

@billing_bp.route("/bill/<id>?from=t1&to=t2", methods=["GET"])
def make_bill(id, time_start, time_end):
    data = {} ## future json to return
    """
    this function will make and return a bill

    Expects : id (provider id), time to start, time to endn
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
    
    unique_trucks = BillService.get_unique_trucks(id) ## gets a list
    TruckCount = 0
    SessionCount = 0
    Products = []
    total = 0
    ### request for the session list based on each truck_id
    for truck_id in unique_trucks:
        route = f'/truck/{truck_id}/session?from={time_start}&to={time_end}'
        response = request.get(route)
        if response.status_code == 200:
            TruckCount += 1
            
            ### traverse the sessions.
            for session in (response.json())["sessions"]:
                SessionCount += 1
                
                sesion_route= f'{WEIGHT_SERVICE_URL}/session/{session}'
                session_response = request.get(sesion_route)
                if session_response.status_code == 200:
                    
                    res = session_response.json()
                    data = BillService.initialize_product_entry(res["produce"])
                    
                    
                    ### check if the product already exists in the list 
                    ### and sum the count and amout if not create it

                    for prod in Products:
                        ###check with wieght team if produce or prodcut.
                        if prod["produce"] == res["produce"]:
                            prod["count"] += 1
                            prod["amount"] += res["neto"]
                            break  
                        
                        data["count"] += 1
                        prod["amount"] += res["neto"]
                        Products.append(data)
                    

    ### find rates
    for product in Products:
        product["rate"] = BillService.get_rates_by_product(prod["produce"])
        product["pay"] = product["rate"] * product["amount"]
        total += product["pay"]
    
    
    data = {
        "id": id,
        "name": "name",
        "from": time_start,
        "to": time_end,
        "truckCount": TruckCount,
        "sessionCount": SessionCount,
        "products": Products,
        "total": total
    }

    return jsonify(data),200


