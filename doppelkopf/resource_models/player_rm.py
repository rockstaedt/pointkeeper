from typing import Dict
from sqlalchemy import func

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

def get_game_statistic_player(player_id) -> Dict:
    player = Player.query.get(player_id)
    game_statistics = {
        "total_points": player.total_points,
        "total_games": player.total_games,
        "points_game_ration": round(player.points_game_ration, 2),
        "ranking": player.ranking
    }
    return game_statistics