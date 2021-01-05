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
from sqlalchemy import select, desc, func, extract
import os

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

from doppelkopf.resource_models import (
    result_rm,
    player_rm,
    game_rm
)

ui_basis = Blueprint('ui_basis', __name__)

# @ui_basis.route('/home', methods = ['GET'])
# # @basis.route('/#spielliste', methods = ['GET'])
# # @basis.route('/#rangliste', methods = ['GET'])
# def home():
#     games = Game.query.order_by(Game.date).all()
#     players = Player.query.order_by(Player.name).all()
#     player_results = {}
#     for game in games:
#         player_results[game.id] = result_rm.get_player_results(
#             game_id = game.id
#         )
#     player_statistics = {}
#     for player in players:
#         # update here again because one player is always missing
#         # in game update / save / delete
#         player_rm.update_game_statistics(player.id)
#         db.session.commit()
#         player_statistics[player.id] = player_rm.get_game_statistic_player(
#             player.id
#         )
#     players_ranked = Player.query.order_by(Player.ranking).all()
#     # return render_template('index.html',
#     #     games = games,
#     #     players = players,
#     #     players_ranked  = players_ranked,
#     #     player_results = player_results,
#     #     player_statistics =  player_statistics
#     # )

@ui_basis.route('/')
def start():
    return render_template('start.html')

@ui_basis.route('/home')
def home():
    # get players
    players = Player.query.order_by(Player.name).all()
    # get counter for games
    games= Game.query.order_by(Game.date).all()
    games_count = len(games)
    # get player with most points
    player_most_points = Player.query.order_by(
        desc(Player.points_game_ration)
    ).first()
    # get player with most played games
    player_id_to_total_games = result_rm.get_total_games_all()
    player_most_games = Player.query.get(max(
        player_id_to_total_games,
        key=player_id_to_total_games.get)
    )
    # get player with most wins
    player_id_to_wins = result_rm.get_counter_placement_all(1)
    player_most_wins = Player.query.get(max(
        player_id_to_wins,
        key=player_id_to_wins.get)
    )
    player_id_to_defeats = result_rm.get_counter_placement_all(-1)
    player_most_defeats = Player.query.get(max(
        player_id_to_defeats,
        key=player_id_to_defeats.get)
    )
    return render_template(
        'home.html',
        players=players,
        games_count=games_count,
        player_most_points=player_most_points,
        player_most_games=(
            player_most_games, player_id_to_total_games[player_most_games.id]
        ),
        player_most_wins=(
            player_most_wins, player_id_to_wins[player_most_wins.id]
        ),
        player_most_defeats=(
            player_most_defeats, player_id_to_defeats[player_most_defeats.id]
        )
    )

@ui_basis.route('/games', methods=['GET'])
def games():
    games = Game.query.order_by(Game.date).all()
    players = Player.query.order_by(Player.name).all()
    player_results = {}
    for game in games:
        player_results[game.id] = result_rm.get_player_results(
            game_id = game.id
        )
    return render_template(
        'games.html',
        player_results=player_results,
        players=players,
        games=games,
        days_for_delete=os.environ['DELETE_DAYS']
    )

@ui_basis.route('/ranking', methods=['GET'])
def ranking():
    result = db.session.query(
        func.min(extract('year', Game.date)).label('year_min'),
        func.max(extract('year', Game.date)).label('year_max')
    ).one()
    years = list(range(int(result.year_max), int(result.year_min)-1, -1))
    player_statistics = {year: {} for year in years}
    player_statistics['ewig'] = player_rm.get_statistics_players()
    for year in years:
        player_statistics[year] = player_rm.get_statistics_players_by_year(year)
    return render_template(
        'ranking.html',
        player_statistics=player_statistics,
        years=years
    )