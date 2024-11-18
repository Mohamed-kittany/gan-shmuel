from flask import Blueprint, request, jsonify
from db import get_db
import uuid
import datetime

bp = Blueprint('post_weight', __name__)

@bp.route('/weight', methods=['POST'])
def post_weight():
    try:
        data = request.json
        print("Received data:", data)
        direction = data.get('direction')
        truck = data.get('truck', 'na')
        containers = data.get('containers', '')
        weight = data.get('weight')
        unit = data.get('unit')
        force = data.get('force', False)
        produce = data.get('produce', 'na')
        
        db = get_db()
        cursor = db.cursor()

        # Check for previous session
        if direction == 'out':
            cursor.execute('SELECT id FROM transactions WHERE truck = %s AND direction = %s ORDER BY datetime DESC LIMIT 1', (truck, 'in'))
            result = cursor.fetchone()
            if not result:
                return jsonify({"error": "No previous 'in' session for truck"}), 400

        # Handle force condition
        if direction in ['in', 'none'] and not force:
            cursor.execute('SELECT id FROM transactions WHERE truck = %s AND direction = %s ORDER BY datetime DESC LIMIT 1', (truck, direction))
            if cursor.fetchone():
                return jsonify({"error": f"{direction} already exists for this truck"}), 400

        session_id = str(uuid.uuid4())

        cursor.execute(
            'INSERT INTO transactions (datetime, direction, truck, containers, bruto, unit, `force`, produce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (datetime.datetime.now(), direction, truck, containers, weight, unit, force, produce)
        )

        if direction == 'out':
            cursor.execute('SELECT bruto FROM transactions WHERE truck = %s AND direction = %s ORDER BY datetime DESC LIMIT 1', (truck, 'in'))
            in_weight = cursor.fetchone()
            if in_weight:
                truck_tara = weight
                neto = in_weight['bruto'] - truck_tara
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
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
