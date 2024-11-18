from flask import Blueprint, jsonify
from db import get_db

bp = Blueprint('get_unknown', __name__)

@bp.route('/unknown', methods=['GET'])
def get_unknown():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM containers_registered WHERE weight IS NULL')
    result = cursor.fetchall()
    unknown_ids = [row['id'] for row in result]
    return jsonify(unknown_ids), 200
