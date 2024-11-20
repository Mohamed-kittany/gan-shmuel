from flask import Blueprint, request, jsonify
from db import get_db
import uuid
import datetime

bp = Blueprint('post_weight', __name__)

@bp.route('/weight', methods=['POST'])
def post_weight():
    direction = request.args.get('direction')
    truck = request.args.get('truck', 'na')
    containers = request.args.get('containers', '')
    weight = request.args.get('weight')
    unit = request.args.get('unit')
    force = request.args.get('force', "false")
    force = force == "true"
    produce = request.args.get('produce', 'na')
        
    db = get_db()
    cursor = db.cursor()
    session_id = str(int(datetime.datetime.now().timestamp()))
    cursor.execute('SELECT direction, session_id FROM transactions WHERE truck = %s ORDER BY datetime DESC LIMIT 1', (truck,))
    result =  cursor.fetchone()
    # when there is no prev rows of this truck
    if not result:
        cursor.execute('INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce, session_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', \
            (datetime.datetime.now(), direction, truck, containers, weight, produce, session_id))
        
    # Handle out condition
    if direction == 'out' and not force:
        if not result or result["direction"] == "out":
            return jsonify({"error": f"{direction} already exists for this truck"}), 400
        elif not result or result["direction"] != "in":
            return jsonify({"error": "No previous 'in' session for truck"}), 400
        if not result:
            session_id = result["session_id"]

    # Handle in condition
    if direction == 'in' and not force:
        if not result or result["direction"] == "in":
            return jsonify({"error": f"{direction} already exists for this truck"}), 400

    # Handle none condition
    if direction == "none":
        if not result or result["direction"] == "in":
            return jsonify({"error": f"{direction} exists for this truck, you can not use none direction"}), 400

    if force == True and (not result or direction == result["direction"]):
        cursor.execute(
            "UPDATE transactions SET datetime = %s, containers = '%s', bruto = '%s', produce = '%s' WHERE truck = %s AND session_id = %s and direction = %s;",
            (datetime.datetime.now(), containers, weight, produce, truck, session_id, direction)
        )
    else:
        cursor.execute('INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce, session_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', \
            (datetime.datetime.now(), direction, truck, containers, weight, produce, session_id))

    if direction == 'out':
        cursor.execute('SELECT bruto FROM transactions WHERE truck = %s AND direction = %s ORDER BY datetime DESC LIMIT 1', (truck, 'in'))
        in_weight = cursor.fetchone()
        if in_weight:
            truck_tara = int(weight)
            neto = int(in_weight["bruto"]) - truck_tara
            cursor.execute('UPDATE transactions SET truckTara = %s, neto = %s WHERE id = %s', (truck_tara, neto, cursor.lastrowid))
        else:
            cursor.execute('UPDATE transactions SET truckTara = %s, neto = NULL WHERE id = %s', (weight, cursor.lastrowid))

    db.commit()

    response = {
        "id": cursor.lastrowid,
        "truck": truck,
        "bruto": weight
    }

    if direction == 'out':
        response.update({"truckTara": truck_tara, "neto": neto if in_weight else "na"})

    return jsonify(response), 201
