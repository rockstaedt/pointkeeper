from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime


from doppelkopf.extensions import db
from doppelkopf.models import Player, Game, Result

form_key_to_description = {
    "date": "das Datum",
    "games": "die gespielten Partien",
    "points_player1": "Punkte Spieler 1",
    "points_player2": "Punkte Spieler 2",
    "points_player3": "Punkte Spieler 3",
    "points_player4": "Punkte Spieler 4",
    "select_player1": "Spieler 1 nicht gewählt.",
    "select_player2": "Spieler 2 nicht gewählt.",
    "select_player3": "Spieler 3 nicht gewählt.",
    "select_player4": "Spieler 4 nicht gewählt.",
}

game = Blueprint('game', __name__)

@game.route('/save_game', methods = ["POST"])
def save_game():
    #  check form
    for key, value in request.form.items():
        if request.form[key] == "":
            flash("Spiel nicht gespeichert!"
                + f" Eintrag für {form_key_to_description[key]} hat gefehlt.",
                "danger"
            )
            return redirect("/#spielliste")
        elif request.form[key] == "-1":
            flash("Spiel nicht gespeichert!"
                + f" {form_key_to_description[key]}",
                "danger"
            )
            return redirect("/#spielliste")

    # create game and add to database
    played_game = Game(
        date = datetime.strptime(request.form["date"], "%Y-%m-%d"),
        played_matches = request.form["games"]
    )
    db.session.add(played_game)

    # create results and add to database
    for i in range(1,5):
        player_id = request.form[f"id_player{i}"]
        player = Player.query.get(player_id)
        player_points = request.form[f"points_player{i}"]
        # create result for player
        result = Result(
            points = player_points,
            game = played_game,
            player = player
        )
        db.session.add(result)
        # update players game statistics
        player.update_game_statistics()
    db.session.commit()
    flash("Spiel gespeichert!", "success")
    return redirect("/#spielliste")

@game.route('/update_game/<id>', methods = ["POST"])
def update_game(id):
    for key, value in request.form.items():
        if request.form[key] == "":
            flash("Spiel nicht geändert!"
                + f" Eintrag für {form_key_to_description[key[7:]]} hat gefehlt.",
                "danger"
            )
            return redirect("/#spielliste")
    # update game
    game_to_update= Game.query.get(id)
    game_to_update.date = datetime.strptime(request.form["update_date"], "%Y-%m-%d")
    game_to_update.played_matches = request.form["update_games"]
    # update results
    for i in range(1,5):
        player_id = request.form[f"update_id_player{i}"]
        player = Player.query.get(player_id)
        player_points = request.form[f"update_points_player{i}"]
        # update players game statistics
        player.update_game_statistics()
        # get result and update
        result = Result.query.filter_by(game_id = id, player_id = player_id).one()
        result.points = player_points
    db.session.commit()

    flash("Spiel geändert!", "success")
    return redirect("/#spielliste")

@game.route('/delete_game/<id>', methods = ["GET"])
def delete_game(id):
    # delete games
    game_to_delete = Game.query.get(id)
    db.session.delete(game_to_delete)
    # delete results
    result_to_delete = Result.__table__.delete().where(Result.game_id == id)
    db.session.execute(result_to_delete)
    # update game statistics
    players = Player.query.all()
    for player in players:
        player.update_game_statistics()
    db.session.commit()
    flash(f"Spiel {id} gelöscht!", "success")
    return redirect("/#spielliste")