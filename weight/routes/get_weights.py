from flask import Blueprint, request, jsonify
from db import get_db
import datetime

bp = Blueprint('get_weights', __name__)

@bp.route('/weight', methods=['GET'])
def get_weights():
    t1 = request.args.get('from', datetime.datetime.now().strftime('%Y%m%d') + '000000')
    t2 = request.args.get('to', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    filters = request.args.get('filter', 'in,out,none').split(',')
    placeholders = ", ".join(["%s"] * len(filters))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM transactions WHERE direction IN {placeholders} AND datetime BETWEEN %s AND %s', (*filters, t1, t2))
    result = cursor.fetchall()
    return jsonify(result), 200
