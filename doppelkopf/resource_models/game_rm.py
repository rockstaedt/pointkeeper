from typing import Dict

from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

def get_total_games_all() -> Dict:
    results = db.session.query(
        Result.player_id,
        func.sum(Game.played_matches).label("total_games_sum")
    ).join(
        Game
    ).group_by(
        Result.player_id
    ).all()
    player_id_to_total_games = {}
    for result in results:
            player_id_to_total_games[result.player_id] = result.total_games_sum
    return player_id_to_total_games