from flask import Blueprint
from db import get_db

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health():
    # db = get_db()
    # cursor = db.cursor()
    try:
        # cursor.execute('SELECT 1')
        return "OK", 200
    except:
        return "Failure", 500
