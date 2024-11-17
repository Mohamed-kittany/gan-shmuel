import mysql.connector
from flask import Flask
from flask import request
# from flask_mysqldb import MySQL
from datetime import datetime

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
        host="w-db"
        user="root",
        password="root",
        database="weight"
    )
    cursor = cconn.cursor()
    cursor.execute(query)
    # create json  response
    # data = [{"id": row[0], "direction": row[2], "bruto": row[5], "neto": row[7], "produce": row[8], "containers": row[4]} for row in results]
    # return jsonify(data)
    print(from_dt,to_dt,direction_str,query)
    return "In Process", 200

if __name__=="__main__":
    app.run()