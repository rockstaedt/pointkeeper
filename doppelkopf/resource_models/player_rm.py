from typing import Dict
from sqlalchemy import func, extract, desc
from collections import OrderedDict

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

from doppelkopf.resource_models import result_rm, game_rm

def get_total_games_player(player_id) -> int:
    results = db.session.query(
        Result.player_id,
        func.sum(Game.played_matches).label("total_games_sum")
    ).join(
        Game
    ).filter(
        Result.player_id == player_id
    ).group_by(
        Result.player_id
    ).first()
    if results:
        return results.total_games_sum
    else:
        return 0

def update_game_statistics(player_id):
    player = Player.query.get(player_id)
    player.total_points = result_rm.get_total_points_player(player.id)
    player.total_games = get_total_games_player(player.id)
    if player.total_games != 0:
        player.points_game_ration = player.total_points/player.total_games
    player_id_to_rank_and_points = result_rm.get_total_points_all_ranked()
    if player.total_points != 0 or player.total_games != 0:
        player.ranking = player_id_to_rank_and_points[player.id]["ranking"]
    else:
        player.ranking = 999
        player.points_game_ration = 0

def get_statistics_players() -> OrderedDict:
    players = Player.query.all()
    for player in players:
        update_game_statistics(player.id)
    results = db.session.query(Player).order_by(Player.ranking).all()
    result_dic = OrderedDict()
    for i, result in enumerate(results):
        result_dic[i] = {
            'player': result,
            "total_points": result.total_points,
            "total_batches": result.total_games,
            "ratio": round(result.points_game_ration, 2),
        }
    return result_dic

def get_statistics_players_by_year(year:int) -> OrderedDict:
    results = db.session.query(
        Result.player_id,
        func.sum(Result.points).label('total_points'),
        func.sum(Game.played_matches).label('total_batches')
    ).join(
        Game
    ).filter(
        extract('year', Game.date) == year
    ).group_by(
        Result.player_id
    ).order_by(
        desc('total_points')
    ).all()
    result_dic = OrderedDict()
    for i, result in enumerate(results):
        result_dic[i+1] = {
            'player': Player.query.get(result.player_id),
            'total_points': result.total_points,
            'total_batches': result.total_batches,
            'ratio': round(result.total_points/result.total_batches, 2)
        }
    return result_dic
