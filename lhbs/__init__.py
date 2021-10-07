from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from lhbs.config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from lhbs import models
    
    from lhbs.view.routes import view
    from lhbs.api.routes import api
    app.register_blueprint(view)
    app.register_blueprint(api)
    
    return app
