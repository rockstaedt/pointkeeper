from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect
)
from datetime import datetime

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

api_ranking = Blueprint('api_ranking', __name__)

@api_ranking.route('/api/v1/update_ranking', methods = ['GET'])
def update_ranking():
    player_name_to_points = Result.get_total_points_player()
    return redirect('/#rangliste')