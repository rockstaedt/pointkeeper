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

api_game = Blueprint('api_game', __name__, url_prefix='/api/v1/games/')


@api_game.route('save_game', methods=['POST'])
def save_game():
    # Safari on Mac does not support date input type. That is why, dates
    # in fomat DD.MM.YYYY are caught.
    if '.' in request.form['date']:
        # input type: text
        game_date = datetime.strptime(
            request.form['date'],
            '%d.%m.%Y'
        )
    else:
        # input type: date
        game_date = datetime.strptime(
            request.form['date'],
            '%Y-%m-%d'
        )
    # create game and add it to database
    played_game = Game(
        date = game_date,
        played_matches = request.form['games']
    )
    db.session.add(played_game)
    # get counter for players
    counter_player = int(list(request.form.keys())[-1].split('_')[-1])
    # create results for all players and add them to the database
    for i in range(1, counter_player+1):
        player_id = request.form[f'id_player_{i}']
        player = Player.query.get(player_id)
        player_points = request.form[f'points_player_{i}']
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
    return redirect('/games')


@api_game.route('update_game/<game_id>', methods=['POST'])
def update_game(game_id):
    # get game from database
    game_to_update= Game.query.get(game_id)
    # if date is not changed, input type is a text and there formatted
    # differently than in the date input field
    if '.' in request.form['date']:
        # input type: text
        game_to_update.date = datetime.strptime(
            request.form['date'],
            '%d.%m.%Y'
        )
    else:
        # input type: date
        game_to_update.date = datetime.strptime(
            request.form['date'],
            '%Y-%m-%d'
        )
    game_to_update.played_matches = request.form['games']
    # get counter for players
    counter_player = int(list(request.form.keys())[-1].split('_')[-1])
    # loop over all players and update results and game statistics
    for i in range(1, counter_player+1):
        player_id = request.form[f'id_player_{i}']
        player_points = request.form[f'points_player_{i}']
        # update players game statistics
        player_rm.update_game_statistics(player_id)
        # get result and update
        result = Result.query.filter_by(
            game_id = game_id,
            player_id = player_id
        ).one()
        result.points = player_points
    db.session.commit()

    flash('Spiel geändert!', 'success')
    return redirect('/games')


@api_game.route('delete_game/<game_id>', methods=['GET'])
def delete_game(game_id):
    # delete games
    game_to_delete = Game.query.get(game_id)
    db.session.delete(game_to_delete)
    # delete results
    result_to_delete = Result.__table__.delete().where(Result.game_id == game_id)
    db.session.execute(result_to_delete)
    # update game statistics
    players = Player.query.all()
    for player in players:
        player_rm.update_game_statistics(player.id)
    db.session.commit()
    flash(f'Spiel {game_id} gelöscht!', 'success')
    return redirect('/games')


@api_game.route('get_game_date/<game_id>', methods=['GET'])
def get_game_date(game_id):
    game = Game.query.get(game_id)
    if game:
        return {'game_date': game.date.strftime('%Y-%m-%d')}
    else:
        # TODO correct error handling
        return 'Bad Request! Game not found.', 400