from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect
)
from datetime import datetime


from doppelkopf.extensions import db

from doppelkopf.models import Player, Game, Result

from doppelkopf.resource_models import player_rm

api_game = Blueprint('api_game', __name__)

@api_game.route('/api/v1/save_game', methods = ['POST'])
def save_game():
    # create game and add to database
    played_game = Game(
        date = datetime.strptime(request.form['date'], '%Y-%m-%d'),
        played_matches = request.form['games']
    )
    db.session.add(played_game)

    # create results and add to database
    for i in range(1,5):
        player_id = request.form[f'id_player{i}']
        player = Player.query.get(player_id)
        player_points = request.form[f'points_player{i}']
        # create result for player
        result = Result(
            points = player_points,
            game = played_game,
            player = player
        )
        db.session.add(result)
        # update players game statistics
        player_rm.update_game_statistics(player_id)
    db.session.commit()
    flash('Spiel gespeichert!', 'success')
    return redirect('/home')

@api_game.route('/update_game/<id>', methods = ['POST'])
def update_game(id):
    # get game from database
    game_to_update= Game.query.get(id)
    game_to_update.date = datetime.strptime(
        request.form['update_date'],
        '%Y-%m-%d'
    )
    game_to_update.played_matches = request.form['update_games']
    # update results
    for i in range(1,5):
        player_id = request.form[f'update_id_player{i}']
        player = Player.query.get(player_id)
        player_points = request.form[f'update_points_player{i}']
        # update players game statistics
        player_rm.update_game_statistics(player_id)
        # get result and update
        result = Result.query.filter_by(
            game_id = id,
            player_id = player_id
        ).one()
        result.points = player_points
    db.session.commit()

    flash('Spiel geändert!', 'success')
    return redirect('/#spielliste')

@api_game.route('/delete_game/<id>', methods = ['GET'])
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
        player_rm.update_game_statistics(player.id)
    db.session.commit()
    flash(f'Spiel {id} gelöscht!', 'success')
    return redirect('/#spielliste')