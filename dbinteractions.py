import mariadb as db
import dbcreds as c

def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(username=c.user, password=c.password, host=c.host, port=c.port, database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except:
        print("Sorry, please try again")

    return conn, cursor

def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except:
        print("Issue closing cursor. Someone should look into this/")
    try:
        conn.close()
    except:
        print("Issue closing connection. Someone should look into this.")

def insert_post(username, content):
    success = False
    id = None
    conn, cursor = connect_db()
    try:
        cursor.execute("INSERT INTO post(username, content) VALUES(?,?)", [username, content,])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    disconnect_db(conn, cursor)
    return success, id

def get_all_posts():
    success = False
    posts = []
    conn, cursor = connect_db()
    try:
        cursor.execute("SELECT id, content, username, created_at FROM post")
        posts = cursor.fetchall()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    disconnect_db(conn, cursor)
    return success, posts