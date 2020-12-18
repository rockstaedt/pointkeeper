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

ranking = Blueprint("ranking", __name__)

@ranking.route("/update_ranking", methods = ["GET"])
def update_ranking():
    player_name_to_points = Result.get_total_points_player()
    print(player_name_to_points)
    return redirect("/#rangliste")