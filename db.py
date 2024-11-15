import sqlite3, os

DataBase = "database.db"
ResultData = "resultDB.db"
IntegrationDB = "IntegrationDB.db"
# if os.path.exists("resultDB.db"):
#    os.remove("resultDB.db")


def create_Title():
    con = sqlite3.connect(DataBase)
    con.execute("CREATE TABLE IF NOT EXISTS BookTitle (Title UNIQUE,qnum,collectans)")
    con.close()

    conR = sqlite3.connect(ResultData)
    conR.execute(
        "CREATE TABLE IF NOT EXISTS ResultList (date,Title,collect,uncollect,accuracy,RD,favo)"
    )
    conR.close()

    con = sqlite3.connect(IntegrationDB)
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
