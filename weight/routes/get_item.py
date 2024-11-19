from flask import Blueprint, request, jsonify
from db import get_db
import datetime

bp = Blueprint('get_item', __name__)

@bp.route('/item/<id>', methods=['GET'])
def get_item(id):
    t1 = request.args.get('from', datetime.datetime.now().replace(day=1).strftime('%Y%m%d') + '000000')
    t2 = request.args.get('to', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    db = get_db()
    cursor = db.cursor()

    # Check if the item exists in trucks
    cursor.execute('SELECT truck, truckTara, id FROM transactions WHERE truck = %s AND datetime BETWEEN %s AND %s', (id, t1, t2))
    truck_results = cursor.fetchall()
    if truck_results:
        tara = truck_results[-1][1]  # Last record's truckTara
        sessions = [row[2] for row in truck_results]
        return jsonify({"id": id, "truck": id, "tara": tara, "sessions": sessions}), 200

    # Check if the item exists in containers
    cursor.execute('SELECT weight FROM containers_registered WHERE container_id = %s', (id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Item not found"}), 404

    tara = result[0] if result[0] else 'na'
    cursor.execute('SELECT id FROM transactions WHERE FIND_IN_SET(%s, containers) AND datetime BETWEEN %s AND %s', (id, t1, t2))
    container_sessions = cursor.fetchall()
    sessions = [row[0] for row in container_sessions]

    return jsonify({"id": id, "tara": tara, "sessions": sessions}), 200
