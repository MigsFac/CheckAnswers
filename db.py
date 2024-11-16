import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

IntegrationDB = os.path.join(DATABASE_DIR, "IntegrationDB.db")
DemoDB = os.path.join(DATABASE_DIR, "DemoDB.db")
# if os.path.exists("IntegrationDB.db"):
#    os.remove("IntegrationDB.db")


def create_Title():
    con = sqlite3.connect(IntegrationDB)
    cur = con.cursor()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
                );
    """
    )
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        password = "admin"
        hashed_pass = generate_password_hash(password)
        cur.execute(
            """
                    INSERT INTO users(username,password,role)
                    VALUES(?,?,?)
                    """,
            ("admin", hashed_pass, "admin"),
        )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS BookTitle(
                book_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id INTEGER,
                Title TEXT,
                qnum,
                collectans,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                );
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS ResultList(
                result_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                book_id INTEGER,
                user_id INTEGER,
                date TEXT,
                Title TEXT,
                collect TEXT,
                uncollect TEXT,
                accuracy TEXT,
                RD TEXT,
                favo TEXT,
                FOREIGN KEY (book_id) REFERENCES BookTitle (book_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                );
                """
    )
    con.commit()
    con.close()

    con = sqlite3.connect(DemoDB)
    cur = con.cursor()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
                );
    """
    )
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        password = "admin"
        hashed_pass = generate_password_hash(password)
        cur.execute(
            """
                    INSERT INTO users(username,password,role)
                    VALUES(?,?,?)
                    """,
            ("admin", hashed_pass, "admin"),
        )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS BookTitle(
                book_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id INTEGER,
                Title TEXT,
                qnum,
                collectans,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                );
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS ResultList(
                result_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                book_id INTEGER,
                user_id INTEGER,
                date TEXT,
                Title TEXT,
                collect TEXT,
                uncollect TEXT,
                accuracy TEXT,
                RD TEXT,
                favo TEXT,
                FOREIGN KEY (book_id) REFERENCES BookTitle (book_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                );
                """
    )
    con.commit()
    con.close()
