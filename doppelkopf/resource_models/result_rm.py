from sqlalchemy import func, desc

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

def get_player_results(game_id: int):
    results = db.session.query(
        Result
    ).join(
        Game
    ).join(
        Player
    ).filter(
        Game.id == game_id
    ).all()
    player_name_to_points = {}
    for result in results:
        player_name_to_points[result.player.name] = result.points
    return player_name_to_points

def get_total_points_all_ranked():
    results = db.session.query(
        Result.player_id,
        func.sum(Result.points).label("total_points_sum")
    ).group_by(
        Result.player_id
    ).order_by(
        desc("total_points_sum")
    ).all()
    player_id_to_rank_and_points= {}
    ranking = 1
    for result in results:
            player_id_to_rank_and_points[result.player_id] = {
                "total_points": result.total_points_sum,
                "ranking": ranking
            }
            ranking += 1
    return player_id_to_rank_and_points

def get_total_points_player(player_id: int) -> int:
    results = db.session.query(
        Result.player_id,
        func.sum(Result.points).label("total_points_sum")
    ).filter(
        Result.player_id == player_id
    ).group_by(
        Result.player_id
    ).order_by(
        desc("total_points_sum")
    ).first()
    if results:
        return results.total_points_sum
    else:
        return 0