from flask import Blueprint, jsonify
from db import get_db

bp = Blueprint('get_session', __name__)

@bp.route('/session/<id>', methods=['GET'])
def get_session(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = %s', (id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Session not found"}), 404

    response = {
        "id": result['id'],
        "truck": result['truck'],
        "bruto": result['bruto'],
        "produce": result['produce']  # Include produce in the response
    }

    if result['direction'] == 'out':
        cursor.execute('SELECT bruto FROM transactions WHERE id = %s AND direction = %s', (result['id'], 'in'))
        in_weight = cursor.fetchone()
        if in_weight:
            truck_tara = result['bruto']
            neto = in_weight['bruto'] - truck_tara
            response.update({"truckTara": truck_tara, "neto": neto})
        else:
            response.update({"truckTara": result['bruto'],"id": result['id'], "neto": "na"})

    return jsonify(response), 200
