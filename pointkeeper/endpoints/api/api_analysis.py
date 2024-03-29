from flask import Blueprint
from sqlalchemy import asc

from pointkeeper.extensions import db

from pointkeeper.models import Player, Game, Result
from pointkeeper.resource_models import result_rm

api_analysis = Blueprint('api_analysis', __name__)


@api_analysis.route('/api/v1/get_data_rangliste', methods=['GET'])
def rangliste_chart():
    result_dict = {
        'labels': [],
        'datasets': []
    }
    datasets_dict = {}
    current_total_points = {}
    games = Game.query.order_by(asc(Game.date), asc(Game.id)).all()
    players = Player.query.all()
    player_names = []
    for i, _ in enumerate(games):
        result_dict['labels'].append(f'Spiel {i+1}')
    for player in players:
        player_names.append(player.name)
        datasets_dict[player.name] = {
            'data': [],
            'pointRadius': [],
            'pointHoverRadius': [],
            'pointHitRadius': [],
            'pointStyle': []
        }
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
            Player.start_date,
            Game.id,
            Game.date,
            Result.points
        ).join(
            Player,
            Game
        ).filter(
            Game.id == game.id
        ).all()
        # update total points to get ranking
        for result in results:
            if result.date >= result.start_date:
                if result.name not in current_total_points:
                    current_total_points[result.name] = 0
                current_total_points[result.name] += result.points
        ranked_players = sorted(
            current_total_points.items(),
            key=lambda item: item[1],
            reverse=True
        )
        ranking = 1
        ranked_player_names = []
        for player in ranked_players:
            ranked_player_names.append(player[0])
            datasets_dict[player[0]]['data'].append(ranking)
            ranking += 1
            # Styles for last entry are set in JS.
            if i != len(games) - 1:
                datasets_dict[player[0]]['pointRadius'].append(2)
                datasets_dict[player[0]]['pointHitRadius'].append(10)
                datasets_dict[player[0]]['pointStyle'].append('circle')

        not_ranked_player_names = list(
            set(ranked_player_names).symmetric_difference(set(player_names))
        )
        for player_name in not_ranked_player_names:
            datasets_dict[player_name]['data'].append(-1)
            datasets_dict[player_name]['pointRadius'].append(2)
            datasets_dict[player_name]['pointHitRadius'].append(10)
            datasets_dict[player_name]['pointStyle'].append('circle')

    for key, value in datasets_dict.items():
        result_dict['datasets'].append({
                'label': key,
                'data': value['data'],
                'pointRadius': value['pointRadius'],
                'pointHitRadius': value['pointHitRadius'],
                'pointStyle': value['pointStyle']
        })
    return result_dict


@api_analysis.route('/api/v1/get_data_punktehistorie', methods=['GET'])
def punkte_chart():
    result_dict = {}
    datasets_dict = {}
    result_dict['labels'] = []
    result_dict['datasets'] = []
    current_total_points = {}
    games = Game.query.order_by(asc(Game.date), asc(Game.id)).all()
    players = Player.query.all()
    # create a list of labels which contains number of the game.
    for i, _ in enumerate(games):
        result_dict['labels'].append(f'Spiel {i+1}')
    for player in players:
        # initiate dictionary for players to get the values for chart js
        datasets_dict[player.name] = {
            'data': [],
            'pointRadius': [],
            'pointHoverRadius': [],
            'pointHitRadius': [],
            'pointStyle': []
        }
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
            Player.start_date,
            Game.id,
            Game.date,
            Result.points
        ).join(
            Player,
            Game
        ).filter(
            Game.id == game.id
        ).all()
        for result in results:
            if result.date >= result.start_date:
                if result.name not in current_total_points:
                    current_total_points[result.name] = 0
                current_total_points[result.name] += result.points
        for player, points in current_total_points.items():
            datasets_dict[player]['data'].append(points)
            datasets_dict[player]['pointRadius'].append(2)
            datasets_dict[player]['pointHitRadius'].append(10)
            datasets_dict[player]['pointStyle'].append('circle')
        for player in players:
            if player.name not in current_total_points:
                datasets_dict[player.name]['data'].append(None)
    for key, value in datasets_dict.items():
        result_dict['datasets'].append(
            {
                'label': key,
                'data': value['data'],
                'pointRadius': value['pointRadius'],
                'pointHitRadius': value['pointHitRadius'],
                'pointStyle': value['pointStyle']
            }
        )
    return result_dict


@api_analysis.route('/api/v1/get_data_loser/<year>', methods=['GET'])
def loser_chart(year):
    """
    This function returns a dictionary containing all relevant information
    to create a bar chart with chart.js to show the downsides of the players.
    Hereby, the downside is shown for a specific year.

    :param year: Specifies the considered year.
    :return: A dictionary to set up a bar chart with chart.js
    """
    player_id_to_defeats = result_rm.get_counter_placement_all(
        placement=-1,
        year=year
    )

    data = {
        'labels': [],
        'values': []
    }
    players = Player.query.order_by(Player.name).all()
    total_sum = 0
    for i, player in enumerate(players):
        data['labels'].append(player.name)
        data['values'].append(player_id_to_defeats[player.id])
        total_sum += player_id_to_defeats[player.id]

    data['total_sum'] = total_sum

    return data
