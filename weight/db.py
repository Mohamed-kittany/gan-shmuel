from flask import g
import pymysql
from config import config

def get_db():
    if 'db' not in g:  # Correct the syntax error here
        g.db = pymysql.connect(
            host=config['MYSQL_DATABASE_HOST'],
            user=config['MYSQL_DATABASE_USER'],
            password=config['MYSQL_DATABASE_PASSWORD'],
            database=config['MYSQL_DATABASE_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        initialize_db(g.db)  # Initialize the database schema
    return g.db

def initialize_db(db):
    cursor = db.cursor()
    # Create containers_registered table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS containers_registered (
        container_id VARCHAR(15) NOT NULL,
        weight INT(12) DEFAULT NULL,
        unit VARCHAR(10) DEFAULT NULL,
        PRIMARY KEY (container_id)
    ) ENGINE=MyISAM AUTO_INCREMENT=10001;
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INT(12) NOT NULL AUTO_INCREMENT,
        datetime DATETIME DEFAULT NULL,
        direction VARCHAR(10) DEFAULT NULL,
        truck VARCHAR(50) DEFAULT NULL,
        containers VARCHAR(10000) DEFAULT NULL,
        bruto INT(12) DEFAULT NULL,
        truckTara INT(12) DEFAULT NULL,
        neto INT(12) DEFAULT NULL,
        produce VARCHAR(50) DEFAULT NULL,
        unit VARCHAR(10) DEFAULT NULL,  -- Add this line
        `force` BOOLEAN NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=MyISAM AUTO_INCREMENT=10001;
    ''')

    db.commit()

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
