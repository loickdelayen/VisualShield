import mysql.connector
from mysql.connector import Error
import threading

DB_LOCK = threading.Lock()

def create_connection(host='localhost', port=3306, user='root', password='', database=None):
    """ create a database connection to the MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return conn

def create_database(conn, database_name):
    """Create database if it does not exist"""
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            conn.commit()
    except Error as e:
        print(f"Error creating database: {e}")

def create_images_table(conn):
    """Create images table if it does not exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS images (
        id INT PRIMARY KEY AUTO_INCREMENT,
        imagem LONGBLOB,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    except Error as e:
        print(f"Error creating images table: {e}")

def create_classes_table(conn):
    """Create classes table if it does not exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS classes (
        id INT PRIMARY KEY AUTO_INCREMENT,
        HARD_HAT_QTN FLOAT,
        GOOGLES_QTN FLOAT,
        GLOOVES_QTN FLOAT
    );
    """
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    except Error as e:
        print(f"Error creating classes table: {e}")

def create_log_table(conn):
    """Create log table if it does not exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS log (
        id INT PRIMARY KEY AUTO_INCREMENT,
        calendario DATETIME,
        state CHAR(1),
        class_id INT,
        image_id INT,
        FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
        FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
    );
    """
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    except Error as e:
        print(f"Error creating log table: {e}")

def create_delete_old_images_event(conn):
    """Create event scheduler to delete old images"""
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute("SET GLOBAL event_scheduler = ON;")
            event_sql = """
            CREATE EVENT IF NOT EXISTS delete_old_images
            ON SCHEDULE EVERY 1 DAY
            STARTS TIMESTAMP(CURRENT_DATE, '18:00:00')
            DO
                DELETE FROM images
                WHERE created_at < NOW() - INTERVAL 15 DAY;
            """
            cursor.execute(event_sql)
            conn.commit()
    except Error as e:
        print(f"Error creating event scheduler: {e}")

def insert_image(conn, image_blob):
    """Insert image blob into images table and return inserted id"""
    sql = "INSERT INTO images (imagem) VALUES (%s)"
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(sql, (image_blob,))
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error inserting image: {e}")
        return None

def insert_class(conn, hard_hat_qtn, googles_qtn, glooves_qtn):
    """Insert class quantities into classes table and return inserted id"""
    sql = "INSERT INTO classes (HARD_HAT_QTN, GOOGLES_QTN, GLOOVES_QTN) VALUES (%s, %s, %s)"
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(sql, (hard_hat_qtn, googles_qtn, glooves_qtn))
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error inserting class: {e}")
        return None

def insert_log(conn, calendario, state, class_id, image_id):
    """Insert log record into log table"""
    sql = "INSERT INTO log (calendario, state, class_id, image_id) VALUES (%s, %s, %s, %s)"
    try:
        with DB_LOCK:
            cursor = conn.cursor()
            cursor.execute(sql, (calendario, state, class_id, image_id))
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error inserting log: {e}")
        return None
