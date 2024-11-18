from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import os
import csv
from db import get_db, close_db

# Import the blueprints
from routes.post_weight import bp as post_weight_bp
from routes.batch_weight import bp as batch_weight_bp
from routes.get_unknown import bp as get_unknown_bp
from routes.get_weights import bp as get_weights_bp
from routes.get_item import bp as get_item_bp
from routes.get_session import bp as get_session_bp
from routes.health import bp as health_bp

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(post_weight_bp)
app.register_blueprint(batch_weight_bp)
app.register_blueprint(get_unknown_bp)
app.register_blueprint(get_weights_bp)
app.register_blueprint(get_item_bp)
app.register_blueprint(get_session_bp)
app.register_blueprint(health_bp)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

app.secret_key = "supersecretkey"  # Necessary for flashing messages
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        process_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded and processed')
        return redirect(url_for('index'))
    else:
        flash('Allowed file types are .csv')
        return redirect(request.url)

def process_csv(filepath):
    db = get_db()
    cursor = db.cursor()
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'id' in row and ('kg' in row or 'lb' in row):
                    unit = 'kg' if 'kg' in row else 'lb'
                    weight = row['kg'] if 'kg' in row else row['lb']
                    cursor.execute(
                        'INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s) '
                        'ON DUPLICATE KEY UPDATE weight=%s, unit=%s',
                        (row['id'], weight, unit, weight, unit)
                    )
                else:
                    print(f"Missing required fields in row: {row}")
        db.commit()
    except Exception as e:
        print(f"Error processing CSV: {e}")

if __name__ == '__main__':
    app.run(debug=True)
