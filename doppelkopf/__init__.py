from flask import Flask

from .extensions import db

from .commands import create_tables

from .endpoints import (
    api_analysis,
    api_game,
    api_ranking,
    ui_basis,
    ui_forms
)

def create_app(config_file = 'settings.py'):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(ui_basis)
    app.register_blueprint(ui_forms)
    app.register_blueprint(api_game)
    app.register_blueprint(api_ranking)
    app.register_blueprint(api_analysis)

    app.cli.add_command(create_tables)

    return app

