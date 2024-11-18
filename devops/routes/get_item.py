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

    # Check if the item exists
    cursor.execute('SELECT weight FROM containers_registered WHERE container_id = %s', (id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Item not found"}), 404

    tara = result['weight'] if result else 'na'
    cursor.execute('SELECT id FROM transactions WHERE (truck = %s OR FIND_IN_SET(%s, containers)) AND datetime BETWEEN %s AND %s', (id, id, t1, t2))
    sessions = [row['id'] for row in cursor.fetchall()]
    return jsonify({"id": id, "tara": tara, "sessions": sessions}), 200
