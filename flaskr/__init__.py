import os

from . import db
from flask import Flask
from . import auth
from . import dashbaord
from . import detection


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["UPLOAD_FOLDER"] = app.config.get("UPLOAD_FOLDER", "static/uploads")
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskkr.sqlite")
    )
    # db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(detection.bp)
    app.register_blueprint(dashbaord.bp)
    app.add_url_rule("/", endpoint="index")
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app
