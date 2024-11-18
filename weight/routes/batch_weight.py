from flask import Blueprint, request, jsonify
from db import get_db
import json

bp = Blueprint('batch_weight', __name__)

@bp.route('/batch-weight', methods=['POST'])
def batch_weight():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    data = file.read().decode('utf-8')
    db = get_db()
    cursor = db.cursor()

    if file.filename.endswith('.csv'):
        rows = data.split('\n')
        for row in rows:
            if not row:
                continue
            cols = row.split(',')
            container_id, weight, unit = cols[0], int(cols[1]), cols[2]
            cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE weight=%s, unit=%s', (container_id, weight, unit, weight, unit))
    elif file.filename.endswith('.json'):
        weights = json.loads(data)
        for entry in weights:
            container_id, weight, unit = entry['container_id'], entry['weight'], entry['unit']
            cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE weight=%s, unit=%s', (container_id, weight, unit, weight, unit))

    db.commit()
    return jsonify({"status": "success"}), 201
