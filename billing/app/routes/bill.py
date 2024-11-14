# bill.py
from flask import Blueprint, jsonify, request, current_app
from app.extensions import get_mysql_connection

bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/bill/<id>', methods=['GET'])
def get_bill(id):
    return id
