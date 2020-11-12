from flask import Blueprint, jsonify
from sqlalchemy import desc, asc, func
from datetime import datetime


from doppelkopf.extensions import db
from doppelkopf.models import Player, Game, Result

analysis = Blueprint('analysis', __name__)

@analysis.route('/rangliste_chart', methods = ["GET"])
def rangliste_chart():
    result_dict = {}
    datasets_dict = {}
    result_dict["labels"] = []
    result_dict["datasets"] = []
    current_total_points = {}
    games = Game.query.order_by(asc(Game.date), asc(Game.id)).all()
    players = Player.query.all()
    for game in games:
        result_dict["labels"].append(game.date.isoformat())
    for player in players:
        datasets_dict[player.name] = {
            "data": [],
            "pointRadius": [],
            "pointHoverRadius": [],
            "pointHitRadius": [],
            "pointStyle": []
        }
        current_total_points[player.name] = 0
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
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
        for result in  results:
            current_total_points[result.name] += result.points
        ranked_players = sorted(
            current_total_points.items(),
            key = lambda item: item[1],
            reverse = True
        )
        ranking = 1
        for player in ranked_players:
            datasets_dict[player[0]]["data"].append(ranking)
            ranking += 1
            if i != len(games) - 1:
                datasets_dict[player[0]]["pointRadius"].append(5)
                datasets_dict[player[0]]["pointHitRadius"].append(5)
                datasets_dict[player[0]]["pointStyle"].append("circle")
        if i == 0:
            # In the first game, one player does not have points -> 5th place
            for player in players:
                if len(datasets_dict[player.name]["data"]) == 0:
                    datasets_dict[player.name]["data"].append(5)
                    datasets_dict[player.name]["pointRadius"].append(5)
                    datasets_dict[player.name]["pointHitRadius"].append(5)
                    datasets_dict[player.name]["pointStyle"].append("circle")
    for key, value in datasets_dict.items():
        result_dict["datasets"].append(
            {
                "label": key,
                "data": value["data"],
                "pointRadius": value["pointRadius"],
                "pointHitRadius": value["pointHitRadius"],
                "pointStyle": value["pointStyle"]
            }
        )
    return jsonify(result_dict)

@analysis.route('/punkte_chart', methods = ["GET"])
def punkte_chart():
    result_dict = {}
    datasets_dict = {}
    result_dict["labels"] = []
    result_dict["datasets"] = []
    current_total_points = {}
    games = Game.query.order_by(asc(Game.date), asc(Game.id)).all()
    players = Player.query.all()
    # create a list of labels which contains the games dates and store it
    # in a dictionary
    for game in games:
        result_dict["labels"].append(game.date.isoformat())
    for player in players:
        # initiate dictionary for players to get the values for chart js
        datasets_dict[player.name] = {
            "data": [],
            "pointRadius": [],
            "pointHoverRadius": [],
            "pointHitRadius": [],
            "pointStyle": []
        }
        current_total_points[player.name] = 0
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
            Game.id,
            Game.date,
            Result.points
        ).join(
            Player,
            Game
        ).filter(
            Game.id == game.id
        ).all()
        for result in  results:
            current_total_points[result.name] += result.points
        for player, points in current_total_points.items():
            datasets_dict[player]["data"].append(points)
            # add properties for chart js without picture
            if i != len(games) - 1:
                datasets_dict[player]["pointRadius"].append(5)
                datasets_dict[player]["pointHitRadius"].append(5)
                datasets_dict[player]["pointStyle"].append("circle")
        # if i == 0:
        #     # In the first game, one player does not have points -> 0 points
        #     for player in players:
        #         if len(datasets_dict[player.name]["data"]) == 0:
        #             datasets_dict[player.name]["data"].append(0)
        #             datasets_dict[player.name]["pointRadius"].append(5)
        #             datasets_dict[player.name]["pointHitRadius"].append(5)
        #             datasets_dict[player.name]["pointStyle"].append("circle")
    for key, value in datasets_dict.items():
        result_dict["datasets"].append(
            {
                "label": key,
                "data": value["data"],
                "pointRadius": value["pointRadius"],
                "pointHitRadius": value["pointHitRadius"],
                "pointStyle": value["pointStyle"]
            }
        )
    return jsonify(result_dict)