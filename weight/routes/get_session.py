from flask import Blueprint, jsonify
from db import get_db

bp = Blueprint('get_session', __name__)

@bp.route('/session/<id>', methods=['GET'])
def get_session(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM transactions WHERE session_id = %s', (id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Session not found"}), 404

    response = {
        "session_id": result[9],
        "truck": result[3],
        "bruto": result[5],
        "produce": result[8]  # Include produce in the response
    }

    if result[2] == 'out':
        cursor.execute('SELECT bruto FROM transactions WHERE session_id = %s AND direction = %s', (result[9], 'in'))
        in_weight = cursor.fetchone()
        if in_weight:
            truck_tara = result[5]
            neto = int(in_weight[0]) - int(truck_tara)
            response.update({"truckTara": truck_tara, "neto": neto})
        else:
            response.update({"truckTara": result[5],"session_id": result[9], "neto": "na"})

    return jsonify(response), 200
