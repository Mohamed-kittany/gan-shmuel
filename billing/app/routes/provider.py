from flask import Blueprint, jsonify, request
from app.extensions import get_mysql_connection as db


provider_bp = Blueprint('provider', __name__, url_prefix="/providers")

@provider_bp.route('/', methods=['GET'])
def get_providers():
    print("IM HERE")
    cursor = db.get_connection().cursor(dictionary=True)
    cursor.execute("SELECT * FROM Provider")
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

@provider_bp.route('/', methods=['POST'])
def create_provider():
    data = request.get_json()
    name = data.get("name")
    cursor = db.get_connection().cursor()
    cursor.execute("INSERT INTO Provider (name) VALUES (%s)", (name,))
    db.get_connection().commit()
    cursor.close()
    return jsonify({"message": "Provider created"}), 201
