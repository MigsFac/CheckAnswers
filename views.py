from flask import Flask, render_template, request, jsonify, redirect, session, url_for

from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3, math, json, os, chardet
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

IntegrationDB = os.path.join(DATABASE_DIR, "IntegrationDB.db")

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/")
def index():
    print("index here")
    return render_template("index.html", current_page="index")


@app.route("/Calculator")
def Calculator():
    if "user_id" in session:
        keep = ["user_id", "userlist"]
        keepdata = {key: session[key] for key in keep if key in session}
        session.clear()
        session.update(keepdata)
    else:
        session.clear()
    return render_template("Calculator.html", current_page="Calculator")


@app.route("/Gchrono")
def Gchrono():
    return render_template("Gchrono.html", current_page="Gchrono")


@app.route("/Gquotes")
def Gquotes():
    return render_template("Gquotes.html", current_page="Gquotes")


@app.route("/dataset")
def dataset():
    return render_template("dataset.html", current_page="dataset")


@app.route("/AIethics")
def AIethics():
    return render_template("AIethics.html", current_page="AIethics")


@app.route("/GLevel")
def GLevel():
    return render_template("GLevel.html", current_page="GLevel")


@app.route("/TestQA")
def TestQA():
    if "user_id" in session:
        keep = ["user_id", "userlist"]
        keepdata = {key: session[key] for key in keep if key in session}
        session.clear()
        session.update(keepdata)
    else:
        session.clear()
    questions = 1  # 問目

    if "user_id" in session:
        con = sqlite3.connect(IntegrationDB)
        BT_db = con.execute(
            "SELECT * FROM BookTitle WHERE user_id =?", (session["user_id"]["user_id"],)
        ).fetchall()
    else:
        con = sqlite3.connect(IntegrationDB)
        BT_db = con.execute("SELECT * FROM DEMOBookTitle").fetchall()
    con.close()

    BookTitle = []
    for row in BT_db:
        BookTitle.append({"Title": row[2], "qnum": row[3], "collectans": row[4]})

    if "questions" not in session:
        session["questions"] = questions
    if "BookTitle" not in session:
        session["BookTitle"] = BookTitle

    return render_template("TestQA.html", current_page="TestQA", BookTitle=BookTitle)


@app.route("/db")
def db():
    if "user_id" in session:
        con = sqlite3.connect(IntegrationDB)
        user_DB = con.execute(
            "SELECT * FROM BookTitle WHERE user_id =?", (session["user_id"]["user_id"],)
        ).fetchall()
        userlist = con.execute("SELECT user_id,username,role FROM users").fetchall()
        session["userlist"] = userlist
        print(userlist)
        con.close()
        BookTitle = []
        for row in user_DB:
            BookTitle.append({"Title": row[2], "qnum": row[3], "collectans": row[4]})

        session["BookTitle"] = BookTitle

    BookT = session.get("BookTitle", [])
    return render_template("db.html", BookT=BookT)


@app.route("/register", methods=["POST"])
def register():
    Title = request.form["Title"]
    qnum = request.form["qnum"]
    collectans = request.form["collectans"]
    check = request.form.getlist("check")
    action = request.form.get("action")

    if action == "del":
        if check:
            if "user_id" in session:
                user_id = session["user_id"]["user_id"]

                con = sqlite3.connect(IntegrationDB)
                cur = con.cursor()
                for i in check:

                    cur.execute(
                        "DELETE FROM BookTitle WHERE Title = ? AND user_id =?",
                        (i, user_id),
                    )
                con.commit()
                db = con.execute(
                    "SELECT * FROM BookTitle WHERE user_id=?",
                    (user_id,),
                ).fetchall()
                con.close()
            else:
                con = sqlite3.connect(IntegrationDB)
                cursor = con.cursor()
                for i in check:
                    cursor.execute("DELETE FROM DEMOBookTitle WHERE Title = ?", (i,))
                con.commit()
                db = con.execute("SELECT * FROM DEMOBookTitle").fetchall()
                con.close()
            Bdb = []
            for row in db:
                Bdb.append({"Title": row[2], "qnum": row[3], "collectans": row[4]})
            session["BookTitle"] = Bdb
        return redirect(url_for("db"))
    elif action == "regist":
        if "user_id" in session:
            con = sqlite3.connect(IntegrationDB)
            con.execute(
                "INSERT INTO BookTitle (user_id,Title,qnum,collectans) VALUES(?,?,?,?)",
                [session["user_id"]["user_id"], Title, qnum, collectans],
            )
            con.commit()
            db = con.execute(
                "SELECT * FROM BookTitle WHERE user_id =?",
                (session["user_id"]["user_id"],),
            ).fetchall()
            con.close()
        else:  # ひとまずデモ用にログインしてないときはデモデータベース（ユーザーadminのみでログインなし）使用
            con = sqlite3.connect(IntegrationDB)
            user_id = con.execute(
                "SELECT user_id FROM DEMOusers WHERE username = ?", ("admin",)
            ).fetchone()[0]
            con.execute(
                "INSERT INTO DEMOBookTitle (user_id,Title,qnum,collectans) VALUES(?,?,?,?)",
                [user_id, Title, qnum, collectans],
            )
            con.commit()
            db = con.execute("SELECT * FROM DEMOBookTitle").fetchall()
            con.close()
        Bdb = []
        for row in db:
            Bdb.append({"Title": row[2], "qnum": row[3], "collectans": row[4]})

        session["BookTitle"] = Bdb
        return redirect(url_for("db"))
    return redirect(url_for("db"))


@app.route("/cossim")
def cossim():
    result = None
    if "result" not in session:
        session["result"] = result

    return render_template("cossim.html")


@app.route("/euclid")
def euclid():
    result = None
    if "result" not in session:
        session["result"] = result
    return render_template("euclid.html")


@app.route("/confumix")
def confumix():
    result = None
    if "result" not in session:
        session["result"] = result
    return render_template("confumix.html")


@app.route("/FMap")
def FMap():
    result = None
    selectedmap = [9, 16, 25, 36]
    selectedfilter = [4, 9]
    if "result" not in session:
        session["result"] = result
    FResult = session["result"]
    return render_template(
        "FeatureMap.html",
        selectedmap=selectedmap,
        selectedfilter=selectedfilter,
        FResult=FResult,
    )


@app.route("/result", methods=["POST"])
def result():
    kinds = request.form.get("submit")
    cossim = None
    cossiminit = []
    euclid = None
    euclidinit = []
    confumix = []
    confuinit = []
    Accuracy = None
    Precision = None
    Recall = None
    F_measure = None
    ResultFlat = []
    parainit = []
    Listinit = []
    MapTotal = 0
    if kinds == "cossim":
        ab123 = ["a1", "a2", "a3", "b1", "b2", "b3"]
        values = {
            var: float(request.form.get(var, 0)) if request.form.get(var) else 0
            for var in ab123
        }
        a1, a2, a3, b1, b2, b3 = (
            values["a1"],
            values["a2"],
            values["a3"],
            values["b1"],
            values["b2"],
            values["b3"],
        )

        a1b1 = a1 * b1
        a2b2 = a2 * b2
        a3b3 = a3 * b3

        ar = (a1**2 + a2**2 + a3**2) ** 0.5
        br = (b1**2 + b2**2 + b3**2) ** 0.5

        if ar == 0 or br == 0:
            cossim = "error"
        else:
            cossim = (a1b1 + a2b2 + a3b3) / (ar * br)

        cossiminit = [a1, a2, a3, b1, b2, b3]

        session["result"] = {
            "cossim": cossim,
            "cossiminit": cossiminit,
            "euclid": euclid,
            "euclidinit": euclidinit,
            "confumix": confumix,
            "confuinit": confuinit,
            "ResultFlat": ResultFlat,
            "MapTotal": MapTotal,
            "parainit": parainit,
            "Listinit": Listinit,
        }

        return redirect(url_for("cossim"))

    elif kinds == "euclid":
        ab123 = ["a1", "a2", "a3", "b1", "b2", "b3"]
        values = {
            var: float(request.form.get(var, 0)) if request.form.get(var) else 0
            for var in ab123
        }
        a1, a2, a3, b1, b2, b3 = (
            values["a1"],
            values["a2"],
            values["a3"],
            values["b1"],
            values["b2"],
            values["b3"],
        )

        euclid = ((b1 - a1) ** 2 + (b2 - a2) ** 2 + (b3 - a3) ** 2) ** 0.5

        euclidinit = [a1, a2, a3, b1, b2, b3]

        session["result"] = {
            "cossim": cossim,
            "cossiminit": cossiminit,
            "euclid": euclid,
            "euclidinit": euclidinit,
            "confumix": confumix,
            "confuinit": confuinit,
            "ResultFlat": ResultFlat,
            "MapTotal": MapTotal,
            "parainit": parainit,
            "Listinit": Listinit,
        }
        return redirect(url_for("euclid"))

    elif kinds == "confumix":
        TNFP = ["TP", "FN", "FP", "TN"]
        values = {
            var: int(request.form.get(var, 0)) if request.form.get(var) else 0
            for var in TNFP
        }
        TP, FN, FP, TN = values["TP"], values["FN"], values["FP"], values["TN"]

        if FP == 0 and TP == 0:
            Precision = "error"
        else:
            Precision = round((TP / (FP + TP)), 3)

        if FN == 0 and TP == 0:
            Recall = "error"
        else:
            Recall = round((TP / (FN + TP)), 3)

        if TP == 0 and TN == 0 and FP == 0 and FN == 0:
            Accuracy = "error"
        else:
            Accuracy = round((TN + TP) / (TP + TN + FP + FN), 3)

        if Precision == "error" or Recall == "error":
            F_measure = "error"
        else:
            F_measure = round((2 * Precision * Recall) / (Precision + Recall), 3)

        confumix = [Accuracy, Precision, Recall, F_measure]

        confuinit = [TP, FN, FP, TN]

        session["result"] = {
            "cossim": cossim,
            "cossiminit": cossiminit,
            "euclid": euclid,
            "euclidinit": euclidinit,
            "confumix": confumix,
            "confuinit": confuinit,
            "ResultFlat": ResultFlat,
            "MapTotal": MapTotal,
            "parainit": parainit,
            "Listinit": Listinit,
        }
        return redirect(url_for("confumix"))

    elif kinds == "FM":
        padding = int(request.form.get("pad"))
        stride = int(request.form.get("stride"))
        Mapsize = int(request.form.get("Maps"))
        Filtersize = int(request.form.get("filter"))
        MapList = []
        FilterList = []
        parainit = [padding, stride, Mapsize, Filtersize]

        for i in range(0, Mapsize * Mapsize):
            value = request.form.get(f"ori_{i+1}")
            if value:
                MapList.append(value)
            else:
                MapList.append(0)
        for i in range(0, Filtersize * Filtersize):
            value = request.form.get(f"fil_{i+1}")
            if value:
                FilterList.append(value)
            else:
                FilterList.append(0)

        OriMapList = np.zeros((Mapsize, Mapsize))
        OriMapList = np.array(MapList).reshape(Mapsize, Mapsize)
        FilMapList = np.zeros((Filtersize, Filtersize))
        FilMapList = np.array(FilterList).reshape(Filtersize, Filtersize)

        if padding == 1:
            OriMapListPad = np.zeros((Mapsize + 2, Mapsize + 2))
            for i in range(Mapsize):
                for j in range(Mapsize):
                    OriMapListPad[i + 1][j + 1] = OriMapList[i][j]
            OriMapList = OriMapListPad

        Outputsize = (((Mapsize + padding * 2) - Filtersize) / stride) + 1
        Outputsize = math.floor(Outputsize)
        ResultMap = np.zeros((Outputsize, Outputsize))
        ResultMap1D = []
        nj = 0
        for i in range(0, Outputsize * stride, stride):
            for j in range(0, Outputsize * stride, stride):
                Submatrix = OriMapList[i : Filtersize + i, j : Filtersize + j]
                Adamal = Submatrix.astype(np.int64) * FilMapList.astype(np.int64)
                AdamalPlus = np.sum(Adamal)
                AdamalPlus = AdamalPlus.astype(np.int64)
                AdamalPlus = AdamalPlus.tolist()
                ResultMap1D.append(AdamalPlus)

        ResultMap1D = json.dumps(ResultMap1D)
        ResultMap1D = json.loads(ResultMap1D)

        for i in ResultMap1D:
            MapTotal = MapTotal + i

        Listinit = [MapList, FilterList]
        Listinit = json.dumps(Listinit)
        ResultFlat = ResultMap1D

        session["result"] = {
            "cossim": cossim,
            "cossiminit": cossiminit,
            "euclid": euclid,
            "euclidinit": euclidinit,
            "confumix": confumix,
            "confuinit": confuinit,
            "ResultFlat": ResultFlat,
            "MapTotal": MapTotal,
            "parainit": parainit,
            "Listinit": Listinit,
        }

        return redirect(url_for("FMap"))


@app.route("/Question", methods=["GET", "POST"])
def Question():
    selectBT = request.form.get("QTitle")
    session["selectBT"] = selectBT
    BookTitle = session.get("BookTitle", [])
    qnum = 0
    for book in BookTitle:
        if selectBT == book["Title"]:
            qnum = book["qnum"]
    Rdb = []
    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        con = sqlite3.connect(IntegrationDB)
        R_db = con.execute(
            "SELECT * FROM ResultList WHERE user_id=?", (user_id,)
        ).fetchall()
        bookid = con.execute(
            "SELECT * FROM BookTitle WHERE user_id=?", (user_id,)
        ).fetchall()
        con.close()
        bookid = bookid or []
        book_id = None
        for bi in bookid:
            if selectBT == bi[2]:  # 2title
                book_id = bi[0]  # 0book_id
        if book_id is not None:
            session["book_id"] = book_id
        for row in R_db:
            Rdb.append(
                {
                    "date": row[3],
                    "title": row[4],
                    "collect": row[5],
                    "uncollect": row[6],
                    "accuracy": row[7],
                    "RD": row[8],
                    "favo": row[9],
                }
            )
    else:
        con = sqlite3.connect(IntegrationDB)
        R_db = con.execute("SELECT * FROM DEMOResultList").fetchall()
        bookid = con.execute("SELECT * FROM DEMOBookTitle").fetchall()
        con.close()
        book_id = None
        bookid = bookid or []
        for bi in bookid:
            if selectBT == bi[2]:  # 2title
                book_id = bi[0]  # 0book_id
        if book_id is not None:
            session["book_id"] = book_id
        for row in R_db:
            Rdb.append(
                {
                    "date": row[3],
                    "title": row[4],
                    "collect": row[5],
                    "uncollect": row[6],
                    "accuracy": row[7],
                    "RD": row[8],
                    "favo": row[9],
                }
            )
    session["Rdb"] = Rdb

    qnum = int(qnum)
    session["qnum"] = qnum
    if "myans" not in session:
        session["myans"] = [None] * (qnum + 1)

    if "favo" not in session:
        session["favo"] = [None] * (qnum + 1)

    if request.form.get("action") == "start":
        return render_template("Question.html")
    elif request.form.get("action") == "config":
        return redirect(url_for("db"))
    elif request.form.get("action") == "result":
        return render_template("resultlist.html")


@app.route("/Que2nd", methods=["GET", "POST"])
def Que2nd():
    questions = session["questions"]
    myans = session["myans"]
    favo = session["favo"]

    if request.json.get("prepos") == "preQ":
        questions = questions - 1

    elif request.json.get("prepos") == "postQ":
        questions = questions + 1

    session["questions"] = questions
    session["myans"] = myans
    session["favo"] = favo

    return render_template("Question.html")


@app.route("/saveradio", methods=["POST"])
def saveradio():
    data = request.json
    selected_radio = data.get("selectedRadio")
    selected_check = data.get("selectedCheck")

    myans = session["myans"]
    favo = session["favo"]
    questions = session["questions"]

    if selected_check is None:
        favo[questions] = False
    else:
        favo[questions] = selected_check
    session["favo[questions]"] = favo

    if selected_radio is not None:
        myans[session["questions"]] = int(selected_radio)
    else:
        myans[session["questions"]] = None
    session["myans[questions]"] = myans

    return jsonify(success=True)


@app.route("/get_latest_answers", methods=["GET"])
def get_latest_answers():
    # 必要なsessionデータを取得して返す
    myans = session["myans"]
    favo = session["favo"]
    latest_data = {"myans": myans, "favo": favo}

    return jsonify(latest_data)


@app.route("/setnum", methods=["POST"])
def setnum():
    try:
        pdata = request.get_json()
        if not pdata or "numb" not in pdata:
            return jsonify({"error": "Invalid pdata"}), 400
        try:
            questions = int(pdata["numb"])
            if questions < 0:
                raise ValueError("Invalid value")
        except ValueError as e:
            return jsonify({"errorval": str(e)}), 400

        session["questions"] = questions
        return redirect(url_for("dummy"))
    except Exception as e:
        app.logger.error(f"Error in setnum: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/dummy")
def dummy():
    return render_template("dummy.html")


@app.route("/score", methods=["POST"])
def score():
    print("now scoring")
    scoring = request.get_json().get("scoring")

    collect = 0
    uncollect = 0
    Accuracy = 0
    resultscore = []
    if scoring == "True":
        myans = session["myans"]
        BookTitle = session["BookTitle"]
        selectBT = session["selectBT"]

        for book in BookTitle:
            if selectBT == book["Title"]:
                collectans = book["collectans"]

        ans = list(str(collectans))

        for i in range(len(myans)):
            if i + 1 <= len(ans):
                if str(myans[i + 1]) != ans[i]:
                    uncollect = uncollect + 1
                    resultscore.append(f"No.{i+1}_select:{myans[i+1]}_collect:{ans[i]}")
                else:
                    collect = collect + 1
        Accuracy = collect / (collect + uncollect)
        Accuracy = round(Accuracy * 100, 1)

        result_data = {
            "Accuracy": Accuracy,
            "collect": collect,
            "uncollect": uncollect,
            "resultscore": resultscore,
        }
        redirect_url = "/resultscore"
        session["result_data"] = result_data

        return jsonify({"redirect": redirect_url})


@app.route("/resultscore", methods=["GET", "POST"])
def resultscore():
    return render_template("resultscore.html")


@app.route("/savelist", methods=["POST"])
def savelist():
    collect = session["result_data"].get("collect")
    uncollect = session["result_data"].get("uncollect")
    accuracy = session["result_data"].get("Accuracy")
    RD = session["result_data"].get("resultscore")
    RD = ",".join(RD)
    uncollect = collect + uncollect  # 辞書に登録するようの値調整
    favo = []
    for index, value in enumerate(session["favo"]):
        if value is True:
            favo.append(f"No.{index}")
    favo = ",".join(favo)

    Title = session["selectBT"]
    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        book_id = session["book_id"]
    else:
        book_id = session["book_id"]

    now = datetime.now()
    date = now.strftime("%Y/%m/%d %H:%M:%S")
    print("book_id:", book_id)
    if "user_id" in session:
        con = sqlite3.connect(IntegrationDB)
        con.execute(
            "INSERT INTO ResultList (user_id,book_id,date,Title,collect,uncollect,accuracy,RD,favo) VALUES (?,?,?,?,?,?,?,?,?)",
            [user_id, book_id, date, Title, collect, uncollect, accuracy, RD, favo],
        )
    else:
        con = sqlite3.connect(IntegrationDB)
        user_id = con.execute(
            "SELECT user_id FROM DEMOusers WHERE username = ?", ("admin",)
        ).fetchone()[0]
        con.execute(
            "INSERT INTO DEMOResultList (user_id,book_id,date,Title,collect,uncollect,accuracy,RD,favo) VALUES (?,?,?,?,?,?,?,?,?)",
            [user_id, book_id, date, Title, collect, uncollect, accuracy, RD, favo],
        )
    con.commit()
    con.close

    return jsonify({"redirect_url": "/TestQA"})


@app.route("/delcheck", methods=["POST"])
def delcheck():
    data = request.get_json()
    checkitems = data.get("checkitems", [])
    if not data:
        return jsonify({"error": "Invalid pdata"}), 400
    else:
        if "user_id" in session:
            con = sqlite3.connect(IntegrationDB)
            cursor = con.cursor()
            for item in checkitems:
                cursor.execute("DELETE FROM ResultList WHERE date = ?", (item,))
            user_id = session["user_id"]["user_id"]
            R_db = con.execute(
                "SELECT * FROM ResultList WHERE user_id = ?", (user_id,)
            ).fetchall()
        else:
            con = sqlite3.connect(IntegrationDB)
            cursor = con.cursor()
            for item in checkitems:
                cursor.execute("DELETE FROM DEMOResultList WHERE date = ?", (item,))
            R_db = con.execute("SELECT * FROM DEMOResultList").fetchall()
        con.commit()
        con.close()

        Rdb = []
        for row in R_db:
            Rdb.append(
                {
                    "date": row[3],
                    "title": row[4],
                    "collect": row[5],
                    "uncollect": row[6],
                    "accuracy": row[7],
                    "RD": row[8],
                    "favo": row[9],
                }
            )

        session["Rdb"] = Rdb
        return jsonify({"message": "削除完了", "redirect_url": "/resultlist"})


@app.route("/resultlist", methods=["GET", "POST"])
def resultlist():
    return render_template("resultlist.html")


@app.route("/Glossary", methods=["GET", "POST"])
def Glossary():
    con = sqlite3.connect(IntegrationDB)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        """
        SELECT g.name, g.reading, g.description, t.tag ,L.LargeTag
        FROM glossary g
        JOIN glossary_tags gt ON g.id = gt.glossary_id
        JOIN LargeTags_tags Lt ON Lt.tag_id = t.id
        JOIN tags t ON gt.tag_id = t.id
        JOIN LargeTags L ON L.id = Lt.LargeTag_id
        """
    )
    data = cursor.fetchall()

    cursor.execute("SELECT DISTINCT tag FROM tags")  # tag一覧取得
    tagall = cursor.fetchall()
    taglist = [tag[0] for tag in tagall]
    cursor.execute("SELECT DISTINCT LargeTag FROM LargeTags")  # LargeTag一覧取得
    Ltagall = cursor.fetchall()
    Ltaglist = [Ltag[0] for Ltag in Ltagall]
    cursor.execute(
        """SELECT DISTINCT L.LargeTag, t.tag 
                   FROM LargeTags L
                   JOIN LargeTags_tags Lt ON Lt.LargeTag_id = L.id
                   JOIN tags t ON t.id = Lt.tag_id
                   """
    )
    tagtag = cursor.fetchall()
    con.close()

    terms = {}
    for row in data:
        term_name = row[0]
        term_reading = row[1]
        term_description = row[2]
        tag = row[3]
        Ltag = row[4]

        if term_name not in terms:
            terms[term_name] = {
                "name": term_name,
                "reading": term_reading,
                "description": term_description,
                "tags": [],
                "Ltag": [],
            }
        if tag:
            terms[term_name]["tags"].append(tag)
        if Ltag:
            terms[term_name]["Ltag"].append(Ltag)

    Ltagtag = {}
    for row in tagtag:
        Ltagname = row[0]
        tagname = row[1]
        if Ltagname not in Ltagtag:
            Ltagtag[Ltagname] = {"Ltag": Ltagname, "tag": []}
        if tagname:
            Ltagtag[Ltagname]["tag"].append(tagname)

    return render_template(
        "Glossary.html",
        terms=terms,
        taglist=taglist,
        Ltaglist=Ltaglist,
        Ltagtag=Ltagtag,
        current_page="Glossary",
    )


@app.route("/filein", methods=["GET", "POST"])
def filein():
    data = request.get_json()
    filename = data.get("filein")
    file_path = os.path.join("/Users/joutoushou/flask", filename)
    print(f"Received filname: {filename}")

    with open(file_path, "rb") as f:
        res = chardet.detect(f.read())
        enco = res["encoding"]

    file = pd.read_csv(file_path, encoding=enco)
    print("file:", file)

    con = sqlite3.connect(IntegrationDB)

    for index, row in file.iterrows():
        if filename == "G検定用語集.csv":
            cursor = con.execute(
                """
                INSERT INTO glossary (name,reading,description)
                VALUES (?,?,?);
                """,
                (row["用語"], row["検索用読み"], row["説明"]),
            )
            glossary_id = cursor.lastrowid

            for i in range(1, 5):
                tag = row[f"タグ{i}"]
                if pd.notna(tag):
                    tag = tag.strip()
                    cursor2 = con.execute("SELECT id FROM tags WHERE tag = ?", (tag,))
                    exist_tag = cursor2.fetchone()

                    if exist_tag:
                        tag_id = exist_tag[0]
                    else:
                        cursor2 = con.execute(
                            """
                            INSERT INTO tags (tag)
                            VALUES (?);
                            """,
                            (tag,),
                        )
                        tag_id = cursor2.lastrowid
                    con.execute(
                        "INSERT INTO glossary_tags (glossary_id, tag_id) VALUES (?,?)",
                        (glossary_id, tag_id),
                    )
        elif filename == "largetags.csv":
            LargeTag = row["ラージタグ"]
            Tag = row["タグ"]
            if pd.notna(LargeTag):
                LargeTag = LargeTag.strip()
                cursor = con.execute(
                    "SELECT id FROM LargeTags WHERE LargeTag = ?", (LargeTag,)
                )
                exist_Ltag = cursor.fetchone()

                if (
                    exist_Ltag
                ):  # すでにラージタグの名称があればそのidをなければ新たに登録してそのidを取得
                    Ltag_id = exist_Ltag[0]
                else:
                    cursor = con.execute(
                        """
                    INSERT INTO LargeTags (LargeTag)
                    VALUES (?);
                    """,
                        (LargeTag,),
                    )
                    Ltag_id = cursor.lastrowid
                cursor2 = con.execute(
                    "SELECT id FROM Tags WHERE Tag = ?", (Tag,)
                )  # タグデータベースから該当のタグがあるか、あればそのidをなければエラー返す
                exist_tag = cursor2.fetchone()
                if exist_tag:
                    tag_id = exist_tag[0]
                else:
                    con.close()
                    return jsonify(
                        {
                            "message": "登録されてないタグがあります。先にタグ（用語）登録を"
                        }
                    )
                con.execute(
                    "INSERT INTO LargeTags_tags (LargeTag_id, tag_id) VALUES (?,?)",
                    (Ltag_id, tag_id),
                )

    con.commit()
    con.close()
    return jsonify({"message": "file received"})


@app.route("/userregist", methods=["POST"])
def userregist():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    rolecheck = data.get("rolecheck")

    if rolecheck == True:
        role = "admin"
    else:
        role = "guest"

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400

    hashed_pass = generate_password_hash(password)
    try:
        with sqlite3.connect(IntegrationDB) as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO users (username,password,role) VALUES (?,?,?)",
                (username, hashed_pass, role),
            )
            cursor.execute("SELECT user_id,username,role FROM users")
            userlist = cursor.fetchall()
            session["userlist"] = userlist
            con.commit()

        return jsonify({"message": "User registered successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/deluser", methods=["POST"])
def deluser():
    data = request.get_json()
    checkitems = data.get("checkitems", [])
    print("checkitems:", checkitems)
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    else:
        if "user_id" in session:
            con = sqlite3.connect(IntegrationDB)
            cursor = con.cursor()
            for item in checkitems:
                cursor.execute("DELETE FROM users WHERE username = ?", (item,))
            session["userlist"] = cursor.execute(
                "SELECT user_id,username,role FROM users"
            ).fetchall()
            con.commit()
            con.close()
    return jsonify({"message": "削除完了", "redirect_url": "/db"})


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "ログアウト完了", "redirect_url": "/TestQA"})


@app.route("/login", methods=["POST"])
def login():
    if "user_id" not in session:
        session["user_id"] = None

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400

    con = sqlite3.connect(IntegrationDB)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user[3] == "admin":
        cursor.execute("SELECT user_id,username,role FROM users")
        userlist = cursor.fetchall()
        session["userlist"] = userlist

    con.close()

    if user and check_password_hash(user[2], password):
        session["user_id"] = {"user_id": user[0], "username": user[1], "role": user[3]}

        return (
            jsonify({"message": "ログインに成功しました。", "redirect_url": "/TestQA"}),
            200,
        )
    else:
        return jsonify({"error": f"Database error: {str(sqlite3.Error)}"}), 500
