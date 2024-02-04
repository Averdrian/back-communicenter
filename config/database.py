from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def configure_database(app: Flask, db: SQLAlchemy, DB_URI:str) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    db.create_all()
    Migrate(app, db, directory='src/migrations')
