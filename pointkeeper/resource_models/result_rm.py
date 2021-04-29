from sqlalchemy import func, desc, extract
from typing import Dict

from pointkeeper.extensions import db

from pointkeeper.models import Player, Game, Result


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
    player_id_to_rank_and_points = {}
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


def get_total_batches_all() -> Dict:
    results = db.session.query(
        Result.player_id,
        func.sum(Game.played_matches).label("total_games_sum")
    ).join(
        Game
    ).group_by(
        Result.player_id
    ).all()
    player_id_to_total_batches = {}
    for result in results:
        player_id_to_total_batches[result.player_id] = result.total_games_sum
    return player_id_to_total_batches


def get_total_games_all() -> Dict:
    players = Player.query.all()
    player_id_to_total_games = {
        player.id: 0 for player in players
    }
    for player in players:
        played_games = db.session.query(
            Result.player_id
        ).filter(
            Result.player_id == player.id
        ).all()
        for played_game in played_games:
            player_id_to_total_games[player.id] += 1
    return player_id_to_total_games


def get_counter_placement_all(placement: int, year: int = None) -> Dict:
    """
    This function returns a dictionary of player ids, and the corresponding
    number how many times the player reached the passed placement. When the
    parameter year is specified, the number is determined for this year.

    :param placement: Specifies the ranking.
    :param year: Specifies the considered year. Defaults to None.
    :return: Dictionaries of player ids, and the number of the placement.
    """
    players = Player.query.all()

    # Init dictionary to store the counter.
    player_id_to_placement_counter = {player.id: 0 for player in players}

    if year:
        games = Game.query.filter(extract('year', Game.date) == year)
    else:
        games = Game.query.all()

    for game in games:
        results = Result.query.filter(
            Result.game_id == game.id
        ).order_by(
            desc(Result.points)
        ).all()

        if placement <= len(results):
            if placement != -1:
                # Adapt placement to support 0 based array.
                index = placement - 1
            else:
                # Use python slicing to access the last place.
                index = placement
            player_id_to_placement_counter[results[index].player_id] += 1
        else:
            # Raise an error when a placement is passed that cannot be applied
            # to the current game, e.g. placement 5 but only 4 players.
            raise ValueError(
                f'Placement {placement} can not be determined for '
                + f'{len(results)} results for game {game.id}.'
            )

    return player_id_to_placement_counter
