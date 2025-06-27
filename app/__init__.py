from flask import Flask
from .routes import web
from dotenv import load_dotenv
from .db import db
import os
from pathlib import Path

UPLOAD_FOLDER = Path(os.getcwd() + '/uploads')

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodify.db"
    app.secret_key = os.getenv("SECRET_KEY")   
    app.register_blueprint(web)

    db.init_app(app)

    with app.app_context():
        from .db.models import User, Cart, CartItem, Product
        db.create_all()



    return app