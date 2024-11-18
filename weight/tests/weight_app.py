import mysql.connector
from flask import Flask
from flask import jsonify
from flask import request
# from flask_mysqldb import MySQL
from datetime import datetime

DB_CONFIG = {
    'host': 'w-db',  # The hostname of the MySQL container
    'user': 'root',  # The MySQL username
    'password': 'root',  # The MySQL password
    'database': 'weight',  # The database name
    'port': '3306'  # MySQL port
}


PATH_TO_WDB = "./weight/tmp/weightdb.sql"
DATETIME_FORMAT = "%Y%m%d%H%M%S"
DEFAULT_FILTER  = "in,out,none"

app = Flask(__name__)

# # # Config for DB
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "root"
# app.config["MYSQL_DB"] = "weightdb"

# mysql = MySQL(app)

# def read_sql_file():
#     with open(PATH_TO_WDB, "r") as file:
#         sql_commands = file.read().split(";")

#     cursor = mysql.connection.cursor()
#     for command in sql_commands:
#         command = command.strip()
#         if command:
#             cursor.execute(command)
#     mysql.connection.commit()
#     cursor.close()

# with app.app_context():
#     read_sql_file()

@app.get("/health")
def is_healthy():
    return "OK", 200

@app.get("/weight")
def get_weight():
    # get args
    from_timestamp = request.args.get("from", datetime.now().strftime("%Y%m%d000000"))
    to_timestamp = request.args.get("to", datetime.now().strftime(DATETIME_FORMAT))
    direction = request.args.get("filter",  DEFAULT_FILTER)
    # validate
    from_dt = datetime.strptime(from_timestamp, DATETIME_FORMAT)
    to_dt = datetime.strptime(to_timestamp, DATETIME_FORMAT)
    direction_str = ",".join(["'" + arg + "'" for arg in direction.split(",")])
    
    # get data from db
    query = f"SELECT * FROM transactions  WHERE datetime BETWEEN {from_timestamp} AND {to_timestamp} AND (direction IN ({direction_str}));"
    # Connect to the database
    cconn = mysql.connector.connect(
        host="w-db",
        user="root",
        password="root",
        port="3306",
        database="weight"
    )
    cursor = cconn.cursor()
    results = cursor.execute(query)
    # create json  response
    if results:
        data = [{"id": row[0], "direction": row[2], "bruto": row[5], "neto": row[7], "produce": row[8], "containers": row[4]} for row in results]
    else:
        data = [{"None": "None"}]
    return jsonify(data), 200
    # print(from_dt,to_dt,direction_str,query)
    # return "In Process", 200

if __name__=="__main__":
    app.run()

from flask import send_from_directory
import os
import csv
import json

# In-memory store for demonstration purposes
weights = {}
sessions = {}
unknown_containers = set()
batch_weights = {}

def get_unique_id():
    return datetime.now().strftime(DATETIME_FORMAT)

@app.post("/weight")
def post_weight():
    data = request.json
    direction = data.get("direction", "none")
    truck = data.get("truck", "na")
    containers = data.get("containers", "").split(",")
    weight = int(data.get("weight", 0))
    unit = data.get("unit", "kg")
    force = data.get("force", "false").lower() == "true"
    produce = data.get("produce", "na")

    if direction not in ["in", "out", "none"]:
        return jsonify({"error": "Invalid direction"}), 400

    if direction in ["in", "none"]:
        session_id = get_unique_id()
        if direction == "none" and truck != "na":
            return jsonify({"error": "Truck cannot be specified for 'none'"}), 400

        sessions[truck] = {
            "session_id": session_id,
            "bruto": weight,
            "containers": containers,
            "produce": produce,
        }
        return jsonify({"id": session_id, "truck": truck, "bruto": weight})

    if direction == "out":
        if truck not in sessions:
            return jsonify({"error": "No 'in' record for this truck"}), 400
        if not force and "out" in sessions[truck]:
            return jsonify({"error": "Truck already weighed out. Use force=true to overwrite."}), 400

        session = sessions[truck]
        truck_tara = weight
        neto = session["bruto"] - truck_tara
        session["out"] = {"truckTara": truck_tara, "neto": neto}
        return jsonify({
            "id": session["session_id"],
            "truck": truck,
            "bruto": session["bruto"],
            "truckTara": truck_tara,
            "neto": neto
        })

@app.post("/batch-weight")
def batch_weight():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = os.path.join("./in", file.filename)
    file.save(file_path)

    if file.filename.endswith(".csv"):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                container_id, weight = row[0], int(row[1])
                batch_weights[container_id] = weight

    elif file.filename.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
            for entry in data:
                container_id = entry.get("id")
                weight = entry.get("weight", 0)
                batch_weights[container_id] = weight

    return jsonify({"message": "Batch weights uploaded successfully"})

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert file details into MySQL (you can adapt this to your schema)
        cursor.execute("""
            INSERT INTO containers_registered (container_id, weight, unit)
            VALUES (%s, %s, %s)
        """, ('uploaded_file', 100, 'kg'))  # Replace with actual file data

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'File uploaded successfully!'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.get("/unknown")
def get_unknown():
    return jsonify(list(unknown_containers))

@app.get("/weight")
def filter_weights():
    t1 = request.args.get("from", datetime.now().strftime("%Y%m%d000000"))
    t2 = request.args.get("to", datetime.now().strftime(DATETIME_FORMAT))
    filter_directions = request.args.get("filter", DEFAULT_FILTER).split(",")

    results = []
    for truck, session in sessions.items():
        direction = "out" if "out" in session else "in"
        if direction not in filter_directions:
            continue

        result = {
            "id": session["session_id"],
            "direction": direction,
            "bruto": session["bruto"],
            "neto": session["out"]["neto"] if "out" in session else "na",
            "produce": session["produce"],
            "containers": session["containers"]
        }
        results.append(result)

    return jsonify(results)
