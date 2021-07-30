from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
    app.config['SECRET_KEY'] = "random string"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydata'
    mongo = PyMongo(app)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'mydata',
        'host': 'localhost',
        'port': 27017
    }
    db_mongo = MongoEngine(app)
    db.init_app(app)
    # with app.app_context():
    #     from . import views
    #     return app
    with app.app_context():
        from engg.routes import engg
        from mngmnt.routes import mngmnt
        from routes import root_bp, api_bp
        app.register_blueprint(engg, url_prefix='/engineering')
        app.register_blueprint(mngmnt, url_prefix='/management')
        app.register_blueprint(root_bp, url_prefix='/')
        app.register_blueprint(api_bp, url_prefix='/api')
        return app
    # with app.app_context():
    #     from . import views
    #     return app
    # return app
