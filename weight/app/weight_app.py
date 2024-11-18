from flask import Flask, request, jsonify, g
import pymysql
import datetime
import uuid
import os

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="db",
            user="user",
            password="password",
            database="weights_db",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/weight', methods=['POST'])
def post_weight():
    data = request.json
    direction = data.get('direction')
    truck = data.get('truck', 'na')
    containers = data.get('containers', '')
    weight = data.get('weight')
    unit = data.get('unit')
    force = data.get('force', False)
    produce = data.get('produce', 'na')
    
    db = get_db()
    cursor = db.cursor()

    # Generate session_id
    if direction in ['in', 'none']:
        session_id = str(uuid.uuid4())
    elif direction == 'out':
        # Retrieve session_id of the previous 'in' for the truck
        cursor.execute('SELECT session_id FROM weight WHERE truck = %s AND direction = %s ORDER BY date DESC LIMIT 1', (truck, 'in'))
        result = cursor.fetchone()
        if result:
            session_id = result['session_id']
        else:
            return jsonify({"error": "No previous 'in' session for truck"}), 400
    else:
        return jsonify({"error": "Invalid direction"}), 400

    # Insert logic for force conditions and error handling
    if direction in ['in', 'none']:
        if not force:
            cursor.execute('SELECT id FROM weight WHERE truck = %s AND direction = %s ORDER BY date DESC LIMIT 1', (truck, direction))
            if cursor.fetchone():
                return jsonify({"error": f"{direction} already exists for this truck"}), 400
        cursor.execute(
            'INSERT INTO weight (direction, truck, containers, weight, unit, force, produce, session_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (direction, truck, containers, weight, unit, force, produce, session_id)
        )
    elif direction == 'out':
        if not force:
            cursor.execute('SELECT id FROM weight WHERE truck = %s AND direction = %s ORDER BY date DESC LIMIT 1', (truck, 'out'))
            if cursor.fetchone():
                return jsonify({"error": "out already exists for this truck"}), 400
        cursor.execute(
            'INSERT INTO weight (direction, truck, containers, weight, unit, force, produce, session_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (direction, truck, containers, weight, unit, force, produce, session_id)
        )
    
    db.commit()

    response = {
        "id": cursor.lastrowid,
        "truck": truck,
        "bruto": weight
    }

    if direction == 'out':
        cursor.execute('SELECT weight FROM weight WHERE truck = %s AND direction = %s ORDER BY date DESC LIMIT 1', (truck, 'in'))
        in_weight = cursor.fetchone()
        if in_weight:
            truck_tara = weight
            neto = in_weight['weight'] - truck_tara
            response.update({"truckTara": truck_tara, "neto": neto})
        else:
            response.update({"truckTara": weight, "neto": "na"})

    return jsonify(response), 201

@app.route('/batch-weight', methods=['POST'])
def post_batch_weight():
    file = request.files['file']
    file_path = os.path.join('/in', file.filename)
    file.save(file_path)

    db = get_db()
    cursor = db.cursor()

    if file.filename.endswith('.csv'):
        with open(file_path) as f:
            for line in f:
                id, weight, unit = line.strip().split(',')
                cursor.execute('INSERT INTO container (id, weight, unit) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE weight = %s, unit = %s',
                               (id, weight, unit, weight, unit))
    elif file.filename.endswith('.json'):
        import json
        with open(file_path) as f:
            data = json.load(f)
            for entry in data:
                id = entry['id']
                weight = entry['weight']
                unit = entry['unit']
                cursor.execute('INSERT INTO container (id, weight, unit) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE weight = %s, unit = %s',
                               (id, weight, unit, weight, unit))

    db.commit()
    return jsonify({"status": "success"}), 201

@app.route('/unknown', methods=['GET'])
def get_unknown():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM container WHERE weight IS NULL')
    unknowns = [row['id'] for row in cursor.fetchall()]
    return jsonify(unknowns), 200

@app.route('/weight', methods=['GET'])
def get_weight():
    from_date = request.args.get('from', datetime.datetime.now().strftime('%Y%m%d000000'))
    to_date = request.args.get('to', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    filter_directions = request.args.get('filter', 'in,out,none').split(',')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM weight
        WHERE direction IN %s
        AND date BETWEEN %s AND %s
    ''', (tuple(filter_directions), from_date, to_date))

    weights = cursor.fetchall()
    return jsonify(weights), 200

@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    from_date = request.args.get('from', datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0).strftime('%Y%m%d000000'))
    to_date = request.args.get('to', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    db = get_db()
    cursor