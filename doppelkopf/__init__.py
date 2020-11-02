from flask import Flask

from .extensions import db

from .commands import create_tables

from .routes.basis import basis
from .routes.game import game
from .routes.ranking import ranking
from .routes.analysis import analysis

def create_app(config_file = "settings.py"):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(basis)
    app.register_blueprint(game)
    app.register_blueprint(ranking)
    app.register_blueprint(analysis)

    app.cli.add_command(create_tables)

    return app

