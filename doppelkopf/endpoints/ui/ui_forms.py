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
import os

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

from doppelkopf.resource_models import (
    result_rm,
    player_rm
)

ui_forms = Blueprint('ui_forms', __name__)

@ui_forms.route('/add_game/players/<counter>', methods=['GET'])
def add_game(counter):
    players = Player.query.all()
    return render_template('add_game.html', players=players, counter=int(counter))


@ui_forms.route('/update_game/<game_id>', methods=['GET'])
def update_game(game_id):
    result_dic = {}
    results = Result.query.filter(Result.game_id == game_id).all()
    for i, result in enumerate(results):
        result_dic[result.player_id] = {
            'index': i+1,
            'points': result.points,
            'name': Player.query.get(result.player_id).name,
            'player_id': result.player_id
        }
    game = Game.query.get(game_id)
    return render_template(
        'update_game.html',
        game_id=game_id,
        game_date=game.date.strftime('%d.%m.%Y'),
        game_batches=game.played_matches,
        result_dic=result_dic,
        days_for_delete=os.environ['DELETE_DAYS']
    )