import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

IntegrationDB = os.path.join(DATABASE_DIR, "IntegrationDB.db")

# if os.path.exists("IntegrationDB.db"):
#    os.remove("IntegrationDB.db")


# メインDB
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
    try:
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("admin",))
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
            con.commit()
    except:
        print("Error m:", e)

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

    # DemoDB用
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS DEMOusers (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
                );
    """
    )

    try:
        cur.execute("SELECT COUNT(*) FROM DEMOusers WHERE username = ?", ("admin",))
        if cur.fetchone()[0] == 0:
            password = "admin"
            hashed_pass = generate_password_hash(password)
            cur.execute(
                """
                    INSERT INTO DEMOusers(username,password,role)
                    VALUES(?,?,?)
                    """,
                ("admin", hashed_pass, "admin"),
            )
            con.commit()
    except Exception as e:
        print("Error d:", e)

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS DEMOBookTitle(
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
        CREATE TABLE IF NOT EXISTS DEMOResultList(
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

    # glossaryDB
    con.row_factory = sqlite3.Row
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            reading TEXT,
            description TEXT UNIQUE
        );
    """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT UNIQUE
        );
    """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS LargeTags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            LargeTag TEXT UNIQUE
        );
    """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS glossary_tags(
            glossary_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (glossary_id) REFERENCES glossary (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            PRIMARY KEY (glossary_id, tag_id)
        );
    """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS LargeTags_tags(
            LargeTag_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (LargeTag_id) REFERENCES LargeTags (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            PRIMARY KEY (LargeTag_id, tag_id)
        );
    """
    )
    con.commit()
    con.close()
