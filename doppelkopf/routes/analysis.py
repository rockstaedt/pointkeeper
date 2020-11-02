from flask import Blueprint, jsonify
from sqlalchemy import desc, func
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
    games = Game.query.order_by(Game.date).all()
    players = Player.query.all()
    for game in games:
        result_dict["labels"].append(datetime.strftime(game.date, "%d.%m.%Y"))
    for player in players:
        datasets_dict[player.name] = {
            "data": [],
            "pointRadius": [],
            "pointHoverRadius": [],
            "pointHitRadius": [],
            "pointStyle": []
        }
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
            func.sum(Result.points).label("total_points_sum")
        ).join(
            Player,
            Game
        ).filter(
            Game.date <= game.date
        ).group_by(
            Player.name
        ).order_by(
            desc("total_points_sum")
        ).all()
        ranking = 1
        for result in results:
            datasets_dict[result.name]["data"].append(ranking)
            ranking += 1
            if i != len(games) - 1:
                datasets_dict[result.name]["pointRadius"].append(5)
                datasets_dict[result.name]["pointHitRadius"].append(5)
                datasets_dict[result.name]["pointStyle"].append("circle")
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
    games = Game.query.order_by(Game.date).all()
    players = Player.query.all()
    for game in games:
        result_dict["labels"].append(datetime.strftime(game.date, "%d.%m.%Y"))
    for player in players:
        datasets_dict[player.name] = {
            "data": [],
            "pointRadius": [],
            "pointHoverRadius": [],
            "pointHitRadius": [],
            "pointStyle": []
        }
    for i, game in enumerate(games):
        results = db.session.query(
            Player.name,
            func.sum(Result.points).label("total_points_sum")
        ).join(
            Player,
            Game
        ).filter(
            Game.date <= game.date
        ).group_by(
            Player.name
        ).all()
        for result in results:
            datasets_dict[result.name]["data"].append(result.total_points_sum)
            if i != len(games) - 1:
                datasets_dict[result.name]["pointRadius"].append(5)
                datasets_dict[result.name]["pointHitRadius"].append(5)
                datasets_dict[result.name]["pointStyle"].append("circle")
        if i == 0:
            # In the first game, one player does not have points -> 0 points
            for player in players:
                if len(datasets_dict[player.name]["data"]) == 0:
                    datasets_dict[player.name]["data"].append(0)
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