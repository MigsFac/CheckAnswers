from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
    send_file,
)
from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3, math, json, os, chardet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from sqlalchemy.exc import IntegrityError
from app.initdb import (
    User,
    BookTitle,
    ResultList,
    DEMOUser,
    DEMOBookTitle,
    DEMOResultList,
    Glossary,
    Tags,
    LargeTags,
    GlossaryTags,
    LargeTagsTags,
)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", current_page="index")


@main.route("/app-ads.txt")
def app_ads():
    return send_from_directory("static", "app-ads.txt")


@main.route("/Calculator")
def Calculator():
    if "user_id" in session:
        keep = ["user_id", "userlist"]
        keepdata = {key: session[key] for key in keep if key in session}
        session.clear()
        session.update(keepdata)
    else:
        session.clear()
    return render_template("Calculator.html", current_page="Calculator")


@main.route("/Gchrono")
def Gchrono():
    return render_template("Gchrono.html", current_page="Gchrono")


@main.route("/Gquotes")
def Gquotes():
    return render_template("Gquotes.html", current_page="Gquotes")


@main.route("/dataset")
def dataset():
    return render_template("dataset.html", current_page="dataset")


@main.route("/AIethics")
def AIethics():
    return render_template("AIethics.html", current_page="AIethics")


@main.route("/GLevel")
def GLevel():
    return render_template("GLevel.html", current_page="GLevel")


@main.route("/supportjp")
def supportjp():
    return redirect(
        "https://butternut-beetle-638.notion.site/Q-A-157ff023717a8033a9fcfcb7da55d8de?pvs=4",
        code=301,
    )


@main.route("/supporten")
def supporten():
    return redirect(
        "https://butternut-beetle-638.notion.site/FAQ-157ff023717a8074924cd52b4d5a1add?pvs=4",
        code=301,
    )


@main.route("/contact")
def contact():
    return redirect("https://form.run/@migsfactory-xoPPHC2kzjMrEY72dOxa", code=301)


@main.route("/attendtap_privacyjp")
def atpivacyjp():
    return redirect(
        "https://butternut-beetle-638.notion.site/153ff023717a806a9907db22350efede?pvs=4",
        code=301,
    )


@main.route("/attendtap_privacyen")
def atprivacyen():
    return redirect(
        "https://butternut-beetle-638.notion.site/Privacy-Policy-152ff023717a80d1a24bf4a59cefd221?pvs=4",
        code=301,
    )


@main.route("/TestQA")
def TestQA():
    from app import db

    if "user_id" in session:
        keep = ["user_id", "userlist"]
        keepdata = {key: session[key] for key in keep if key in session}
        session.clear()
        session.update(keepdata)
    else:
        session.clear()
    questions = 1  # 問目

    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        BT_db = db.session.query(BookTitle).filter_by(user_id=user_id).all()
    else:
        BT_db = db.session.query(DEMOBookTitle).all()

    BookTitlelist = []
    for row in BT_db:
        BookTitlelist.append(
            {
                "Title": row.title,
                "qnum": row.qnum,
                "collectans": row.collectans,
            }
        )

    if "questions" not in session:
        session["questions"] = questions
    if "BookTitle" not in session:
        session["BookTitle"] = BookTitlelist

    return render_template(
        "TestQA.html", current_page="TestQA", BookTitlelist=BookTitlelist
    )


@main.route("/db")
def db():
    from app import db

    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        user_DB = db.session.query(BookTitle).filter_by(user_id=user_id).all()
        userlist = db.session.query(User.user_id, User.username, User.role).all()
        userlist = [
            {"user_id": row[0], "username": row[1], "role": row[2]} for row in userlist
        ]
        session["userlist"] = userlist

        BookTitlelist = []
        for row in user_DB:
            BookTitlelist.append(
                {"Title": row.title, "qnum": row.qnum, "collectans": row.collectans}
            )

        session["BookTitle"] = BookTitlelist

    BookT = session.get("BookTitle", [])
    return render_template("db.html", BookT=BookT)


@main.route("/register", methods=["POST"])
def register():
    from app import db

    title = request.form["Title"]
    qnum = request.form["qnum"]
    collectans = request.form["collectans"]
    check = request.form.getlist("check")
    action = request.form.get("action")

    if action == "del":
        if check:
            if "user_id" in session:
                user_id = session["user_id"]["user_id"]
                db.session.query(BookTitle).filter(
                    BookTitle.title.in_(check), BookTitle.user_id == user_id
                ).delete(synchronize_session=False)
                db.session.commit()
                book_title_db = (
                    db.session.query(BookTitle).filter_by(user_id=user_id).all()
                )
            else:
                db.session.query(DEMOBookTitle).filter(
                    DEMOBookTitle.title.in_(check),
                ).delete(synchronize_session=False)
                db.session.commit()
                book_title_db = db.session.query(DEMOBookTitle).all()
            Bdb = []
            for row in book_title_db:
                Bdb.append(
                    {"Title": row.title, "qnum": row.qnum, "collectans": row.collectans}
                )
            session["BookTitle"] = Bdb
        return redirect(url_for("main.db"))
    elif action == "regist":
        if "user_id" in session:
            user_id = session["user_id"]["user_id"]
            new_book = BookTitle(
                user_id=user_id, title=title, qnum=qnum, collectans=collectans
            )
            db.session.add(new_book)
            db.session.commit()
            book_title_db = db.session.query(BookTitle).filter_by(user_id=user_id).all()

        else:  # ひとまずデモ用にログインしてないときはデモデータベース（ユーザーadminのみでログインなし）使用
            user_id = (
                db.session.query(DEMOUser.user_id).filter_by(username="admin").scalar()
            )
            new_book = DEMOBookTitle(
                user_id=user_id, title=title, qnum=qnum, collectans=collectans
            )
            db.session.add(new_book)
            db.session.commit()
            book_title_db = db.session.query(DEMOBookTitle).all()

        Bdb = []
        for row in book_title_db:
            Bdb.append(
                {"Title": row.title, "qnum": row.qnum, "collectans": row.collectans}
            )

        session["BookTitle"] = Bdb
        return redirect(url_for("main.db"))
    return redirect(url_for("main.db"))


@main.route("/cossim")
def cossim():
    result = None
    if "result" not in session:
        session["result"] = result

    return render_template("cossim.html")


@main.route("/euclid")
def euclid():
    result = None
    if "result" not in session:
        session["result"] = result
    return render_template("euclid.html")


@main.route("/confumix")
def confumix():
    result = None
    if "result" not in session:
        session["result"] = result
    return render_template("confumix.html")


@main.route("/FMap")
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


@main.route("/result", methods=["POST"])
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

        return redirect(url_for("main.cossim"))

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
        return redirect(url_for("main.euclid"))

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
        return redirect(url_for("main.confumix"))

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

        return redirect(url_for("main.FMap"))


@main.route("/Question", methods=["GET", "POST"])
def Question():
    from app import db

    selectBT = request.form.get("QTitle")
    session["selectBT"] = selectBT
    BookTitlelist = session.get("BookTitle", [])
    qnum = 0
    for book in BookTitlelist:
        if selectBT == book["Title"]:
            qnum = book["qnum"]
    Rdb = []
    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        R_db = db.session.query(ResultList).filter_by(user_id=user_id).all()
        bookid = db.session.query(BookTitle).filter_by(user_id=user_id).all()
        bookid = bookid or []
        book_id = None
        for bi in bookid:
            if selectBT == bi.title:
                book_id = bi.book_id
        if book_id is not None:
            session["book_id"] = book_id
        for row in R_db:
            Rdb.append(
                {
                    "date": row.date,
                    "title": row.title,
                    "collect": row.collect,
                    "uncollect": row.uncollect,
                    "accuracy": row.accuracy,
                    "RD": row.rd,
                    "favo": row.favo,
                }
            )
    else:
        R_db = db.session.query(DEMOResultList).all()
        bookid = db.session.query(DEMOBookTitle).all()
        book_id = None
        bookid = bookid or []
        for bi in bookid:
            if selectBT == bi.title:
                book_id = bi.book_id
        if book_id is not None:
            session["book_id"] = book_id
        for row in R_db:
            Rdb.append(
                {
                    "date": row.date,
                    "title": row.title,
                    "collect": row.collect,
                    "uncollect": row.uncollect,
                    "accuracy": row.accuracy,
                    "RD": row.rd,
                    "favo": row.favo,
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
        return redirect(url_for("main.db"))
    elif request.form.get("action") == "result":
        return render_template("resultlist.html")


@main.route("/Que2nd", methods=["GET", "POST"])
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


@main.route("/saveradio", methods=["POST"])
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


@main.route("/get_latest_answers", methods=["GET"])
def get_latest_answers():
    # 必要なsessionデータを取得して返す
    myans = session["myans"]
    favo = session["favo"]
    latest_data = {"myans": myans, "favo": favo}

    return jsonify(latest_data)


@main.route("/setnum", methods=["POST"])
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
        return redirect(url_for("main.dummy"))
    except Exception as e:
        pdata.logger.error(f"Error in setnum: {e}")
        return jsonify({"error": "Internal server error"}), 500


@main.route("/dummy")
def dummy():
    return render_template("dummy.html")


@main.route("/score", methods=["POST"])
def score():
    scoring = request.get_json().get("scoring")
    collect = 0
    uncollect = 0
    Accuracy = 0
    resultscore = []
    if scoring == "True":
        myans = session["myans"]
        BookTitlelist = session["BookTitle"]
        selectBT = session["selectBT"]

        for book in BookTitlelist:
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


@main.route("/resultscore", methods=["GET", "POST"])
def resultscore():
    return render_template("resultscore.html")


@main.route("/savelist", methods=["POST"])
def savelist():
    from app import db

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

    if "user_id" in session:
        user_id = session["user_id"]["user_id"]
        new_result = ResultList(
            user_id=user_id,
            book_id=book_id,
            date=date,
            title=Title,
            collect=collect,
            uncollect=uncollect,
            accuracy=accuracy,
            rd=RD,
            favo=favo,
        )
        db.session.add(new_result)
        db.session.commit()

    else:
        user_id = (
            db.session.query(DEMOUser.user_id).filter_by(username="admin").scalar()
        )
        new_result = DEMOResultList(
            user_id=user_id,
            book_id=book_id,
            date=date,
            title=Title,
            collect=collect,
            uncollect=uncollect,
            accuracy=accuracy,
            rd=RD,
            favo=favo,
        )
        db.session.add(new_result)
        db.session.commit()

    return jsonify({"redirect_url": "/TestQA"})


@main.route("/delcheck", methods=["POST"])
def delcheck():
    from app import db

    data = request.get_json()
    checkitems = data.get("checkitems", [])
    if not data:
        return jsonify({"error": "Invalid pdata"}), 400
    else:
        if "user_id" in session:
            user_id = session["user_id"]["user_id"]
            db.session.query(ResultList).filter(
                ResultList.date.in_(checkitems),
            ).delete(synchronize_session=False)
            db.session.commit()
            R_db = db.session.query(ResultList).filter_by(user_id=user_id).all()

        else:
            db.session.query(DEMOResultList).filter(
                DEMOResultList.date.in_(checkitems),
            ).delete(synchronize_session=False)
            db.session.commit()
            R_db = db.session.query(DEMOResultList).all()
            db.session.commit()

        Rdb = []
        for row in R_db:
            Rdb.append(
                {
                    "date": row.date,
                    "title": row.title,
                    "collect": row.collect,
                    "uncollect": row.uncollect,
                    "accuracy": row.accuracy,
                    "RD": row.rd,
                    "favo": row.favo,
                }
            )

        session["Rdb"] = Rdb
        return jsonify({"message": "削除完了", "redirect_url": "/resultlist"})


@main.route("/resultlist", methods=["GET", "POST"])
def resultlist():
    return render_template("resultlist.html")


@main.route("/GlossaryPage", methods=["GET", "POST"])
def GlossaryPage():
    from app import db

    data = (
        db.session.query(
            Glossary.name,
            Glossary.reading,
            Glossary.description,
            Tags.tag,
            LargeTags.large_tag,
        )
        .join(GlossaryTags, Glossary.id == GlossaryTags.glossary_id)
        .join(Tags, GlossaryTags.tag_id == Tags.id)
        .join(LargeTagsTags, Tags.id == LargeTagsTags.tag_id)
        .join(LargeTags, LargeTagsTags.large_tag_id == LargeTags.id)
        .all()
    )

    tagall = db.session.query(Tags.tag).distinct().all()  # tag一覧取得
    taglist = [tag[0] for tag in tagall]
    Ltagall = db.session.query(LargeTags.large_tag).distinct().all()  # LargeTag一覧取得
    Ltaglist = [Ltag[0] for Ltag in Ltagall]
    tagtag = (
        db.session.query(LargeTags.large_tag, Tags.tag)
        .join(LargeTagsTags, LargeTagsTags.large_tag_id == LargeTags.id)
        .join(Tags, LargeTagsTags.tag_id == Tags.id)
        .distinct()
        .all()
    )

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


@main.route("/filein", methods=["GET", "POST"])
def filein():
    from app import db

    data = request.get_json()
    filename = data.get("filein")
    file_path = os.path.join("/Users/joutoushou/flask", filename)

    with open(file_path, "rb") as f:
        res = chardet.detect(f.read())
        enco = res["encoding"]

    file = pd.read_csv(file_path, encoding=enco)

    for index, row in file.iterrows():
        if filename == "G検定用語集.csv":
            new_glossary = Glossary(
                name=row["用語"], reading=row["検索用読み"], description=row["説明"]
            )
            db.session.add(new_glossary)
            db.session.flush()
            glossary_id = new_glossary.id
            db.session.commit()

            for i in range(1, 5):
                tag = row[f"タグ{i}"]
                if pd.notna(tag):
                    tag = tag.strip()
                    exist_tag = db.session.query(Tags.id).filter_by(tag=tag).scalar()

                    if exist_tag:
                        tag_id = exist_tag[0]
                    else:
                        new_tag = Tags(tag=tag)
                        db.session.add(new_tag)
                        db.session.flush()
                        tag_id = new_tag.id
                    new_glossary_tag = GlossaryTags(
                        glossary_id=glossary_id, tag_id=tag_id
                    )
                    db.session.add(new_glossary_tag)
                    db.session.commit()

        elif filename == "largetags.csv":
            LargeTag = row["ラージタグ"]
            tag = row["タグ"]
            if pd.notna(LargeTag):
                LargeTag = LargeTag.strip()
                exist_Ltag = (
                    db.session.query(LargeTags.id)
                    .filter_by(large_tag=LargeTag)
                    .scalar()
                )

                if (
                    exist_Ltag
                ):  # すでにラージタグの名称があればそのidをなければ新たに登録してそのidを取得
                    Ltag_id = exist_Ltag[0]
                else:
                    new_large_tag = LargeTags(large_tag=LargeTag)
                    db.session.add(new_large_tag)
                    db.session.commit()
                    db.session.flush()
                    Ltag_id = new_large_tag.id
                exist_tag = db.session.query(Tags.id).filter_by(tag=tag).scalar()

                if exist_tag:
                    tag_id = exist_tag[0]
                else:
                    return jsonify(
                        {
                            "message": "登録されてないタグがあります。先にタグ（用語）登録を"
                        }
                    )
                new_large_tag_tag = LargeTagsTags(LargeTag_id=Ltag_id, tag_id=tag_id)
                db.session.add(new_large_tag_tag)
                db.session.commit()

    return jsonify({"message": "file received"})


@main.route("/userregist", methods=["POST"])
def userregist():
    from app import db

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
        new_user = User(username=username, password=hashed_pass, role=role)
        db.session.add(new_user)
        db.session.commit()
        userlist = db.session.query(User.user_id, User.username, User.role).all()
        userlist = [
            {"user_id": row[0], "username": row[1], "role": row[2]} for row in userlist
        ]
        session["userlist"] = userlist
        return (
            jsonify({"message": "User registered successfully", "redirect_url": "/db"}),
            200,
        )
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@main.route("/deluser", methods=["POST"])
def deluser():
    from app import db

    data = request.get_json()
    checkitems = data.get("checkitems", [])

    if not data:
        return jsonify({"error": "Invalid data"}), 400
    else:
        if "user_id" in session:
            db.session.query(User).filter(
                User.username.in_(checkitems),
            ).delete(synchronize_session=False)
            db.session.commit()
            userlist = db.session.query(User.user_id, User.username, User.role).all()
            userlist = [
                {"user_id": row[0], "username": row[1], "role": row[2]}
                for row in userlist
            ]
            session["userlist"] = userlist

    return jsonify({"message": "削除完了", "redirect_url": "/db"})


@main.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "ログアウト完了", "redirect_url": "/TestQA"})


@main.route("/login", methods=["POST"])
def login():
    from app import db

    if "user_id" not in session:
        session["user_id"] = None

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400

    user = db.session.query(User).filter_by(username=username).scalar()

    if user.role == "admin":
        userlist = db.session.query(User.user_id, User.username, User.role).all()
        userlist = [
            {"user_id": row[0], "username": row[1], "role": row[2]} for row in userlist
        ]
        session["userlist"] = userlist

    if user and check_password_hash(user.password, password):
        session["user_id"] = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
        }

        return (
            jsonify({"message": "ログインに成功しました。", "redirect_url": "/TestQA"}),
            200,
        )
    else:
        return jsonify({"error": f"Database error: {str(sqlite3.Error)}"}), 500
