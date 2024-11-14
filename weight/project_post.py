from flask import Flask, request, jsonify
import csv
import json
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
# Change these to your MySQL credentials
app.config['MYSQL_HOST'] = 'your_mysql_host'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'your_mysql_user'  # Replace with your MySQL user
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'weight' 

# Initialize MySQL
mysql = MySQL(app)

@app.route('/batch-weight', methods=['POST'])
def batch_weight():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "File not provided"}), 400

    data_to_insert = []

    try:
        # Handling CSV file
        if file.filename.endswith('.csv'):
            file_stream = file.stream  # Directly access the file stream
            reader = csv.reader(file_stream)
            for row in reader:
                # Skip headers or rows that do not match the expected format
                if len(row) < 2 or not row[1].isdigit():
                    continue
                
                container_id = row[0].strip()
                weight = row[1].strip()
                unit = row[2].strip().lower() if len(row) > 2 else 'kg'
                
                # Convert weight based on unit
                try:
                    weight = int(weight)
                    weight_kg = weight if unit == 'kg' else int(weight * 0.453592)
                    data_to_insert.append((container_id, weight_kg))
                except ValueError:
                    # Skip rows with invalid weight values
                    continue

        # Handling JSON file
        elif file.filename.endswith('.json'):
            try:
                data = json.load(file.stream)  # Directly load JSON from file stream
                
                # Assuming the JSON file contains an array of objects with 'container_id' and 'weight'
                for entry in data:
                    container_id = entry.get('container_id')
                    weight = entry.get('weight')
                    unit = entry.get('unit', 'kg').lower()  # Default unit is kg if not specified
                    
                    # Process the weight (same logic as for CSV)
                    try:
                        weight = int(weight)
                        weight_kg = weight if unit == 'kg' else int(weight * 0.453592)
                        data_to_insert.append((container_id, weight_kg))
                    except ValueError:
                        # Skip entries with invalid weight values
                        continue
            except Exception as e:
                return jsonify({"error": f"Error reading JSON file: {str(e)}"}), 500

        else:
            return jsonify({"error": "Unsupported file format"}), 400

        # Insert data into the database (MySQL)
        cur = mysql.connection.cursor()
        
        for container_id, weight_kg in data_to_insert:
            try:
                # Insert data into MySQL table (adjust table and column names as necessary)
                cur.execute("INSERT INTO batch_weights (container_id, weight_kg) VALUES (%s, %s)", 
                            (container_id, weight_kg))
            
            except Exception as e:
                return jsonify({"error": f"Error inserting data into the database: {str(e)}"}), 500
        
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Batch data processed and stored successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
