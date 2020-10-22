from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime


from doppelkopf.extensions import db
from doppelkopf.models import Player, Game, Result

basis = Blueprint('basis', __name__)

@basis.route('/home', methods = ["GET"])
@basis.route('/', methods = ["GET"])
@basis.route("/#spielliste", methods = ["GET"])
@basis.route("/#rangliste", methods = ["GET"])
def home():
    games = Game.query.order_by(Game.date).all()
    players = Player.query.order_by(Player.name).all()
    player_results = {}
    for game in games:
        player_results[game.id] = Result.get_player_results(
            game_id = game.id
        )
    player_statistics = {}
    for player in players:
        # update here again because one player is always missing
        # in game update / save / delete
        player.update_game_statistics()
        db.session.commit()
        player_statistics[player.id] = player.get_game_statistic_player()
    players_ranked = Player.query.order_by(Player.ranking).all()
    return render_template("index.html",
        games = games,
        players = players,
        players_ranked  = players_ranked,
        player_results = player_results,
        player_statistics =  player_statistics
    )
