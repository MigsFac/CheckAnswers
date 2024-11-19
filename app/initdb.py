import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from sqlalchemy.exc import IntegrityError
from . import db


# メインDB
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(
        db.String(80),
        nullable=False,
        unique=True,
    )
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class BookTitle(db.Model):
    __tablename__ = "BookTitle"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=True,
    )
    title = db.Column("Title", db.String(255), nullable=True)
    qnum = db.Column(db.Integer, nullable=True)
    collectans = db.Column(db.Integer, nullable=True)


class ResultList(db.Model):
    __tablename__ = "ResultList"
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey("BookTitle.book_id"), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    date = db.Column(db.String(255), nullable=False)
    title = db.Column("Title", db.String(255), nullable=True)
    collect = db.Column(db.Integer, nullable=True)
    uncollect = db.Column(db.Integer, nullable=True)
    accuracy = db.Column(db.Integer, nullable=True)
    rd = db.Column("RD", db.String(255), nullable=True)
    favo = db.Column(db.String(255), nullable=True)


class DEMOUser(db.Model):
    __tablename__ = "DEMOusers"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class DEMOBookTitle(db.Model):
    __tablename__ = "DEMOBookTitle"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("DEMOusers.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    title = db.Column("Title", db.String(255), nullable=False, unique=True)
    qnum = db.Column(db.Integer, nullable=False)
    collectans = db.Column(db.Integer, nullable=False)


class DEMOResultList(db.Model):
    __tablename__ = "DEMOResultList"
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    book_id = db.Column(
        db.Integer,
        db.ForeignKey("DEMOBookTitle.book_id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("DEMOusers.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    date = db.Column(db.String(255), nullable=False)
    title = db.Column("Title", db.String(255), nullable=True)
    collect = db.Column(db.Integer, nullable=True)
    uncollect = db.Column(db.Integer, nullable=True)
    accuracy = db.Column(db.Integer, nullable=True)
    rd = db.Column("RD", db.String(255), nullable=True)
    favo = db.Column(db.String(255), nullable=True)


class Glossary(db.Model):
    __tablename__ = "glossary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    reading = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)


class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)


class LargeTags(db.Model):
    __tablename__ = "LargeTags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    large_tag = db.Column("LargeTag", db.String(255), unique=True, nullable=False)


class GlossaryTags(db.Model):
    __tablename__ = "glossary_tags"
    glossary_id = db.Column(
        db.Integer,
        db.ForeignKey("glossary.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )


class LargeTagsTags(db.Model):
    __tablename__ = "LargeTags_tags"
    large_tag_id = db.Column(
        "LargeTag_id",
        db.Integer,
        db.ForeignKey("LargeTags.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )


def initialize_DB(app):

    db.create_all()
    # adminユーザがいない場合の追加。
    admin_name = "admin"
    admin_pass = "admin"
    try:
        admin_user = User.query.filter_by(username=admin_name).first()
        if not admin_user:
            hashed_pass = generate_password_hash(admin_pass)
            admin_user = User(username="admin", password=hashed_pass, role="admin")
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user added to {User}")
        else:
            print(f"Admin user already exists in {User}")
    except IntegrityError as e:
        db.session.rollback()
        print("Error while creating admin user:", e)

    try:
        Demoadmin_user = DEMOUser.query.filter_by(username=admin_name).first()
        if not admin_user:
            hashed_pass = generate_password_hash(admin_pass)
            Demoadmin_user = DEMOUser(
                username="admin", password=hashed_pass, role="admin"
            )
            db.session.add(Demoadmin_user)
            db.session.commit()
            print(f"Admin user added to {DEMOUser}")
        else:
            print(f"Admin user already exists in {DEMOUser}")
    except IntegrityError as e:
        db.session.rollback()
        print("Error while creating admin user:", e)
