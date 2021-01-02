from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect
)
from datetime import datetime
import pandas as pd
from sqlalchemy import select

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

from doppelkopf.resource_models import (
    result_rm,
    player_rm
)

ui_forms = Blueprint('ui_forms', __name__)

@ui_forms.route('/save_game', methods=['GET'])
def add_game():
    players = Player.query.all()
    return render_template('save_game.html', players=players)