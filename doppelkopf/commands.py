import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Player, Game, Result

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

    eric = Player(
        name = "Eric"
    )
    lucas = Player(
        name = "Lucas"
    )
    marco = Player(
        name = "Marco"
    )
    nils = Player(
        name = "Nils"
    )
    peer = Player(
        name = "Peer"
    )

    db.session.add(eric)
    db.session.add(lucas)
    db.session.add(marco)
    db.session.add(nils)
    db.session.add(peer)

    game = Game(played_matches = 10)

    db.session.add(game)

    result_eric = Result(
        player = eric,
        game = game,
        points = 10
    )

    result_lucas = Result(
        player = lucas,
        game = game,
        points = 12
    )

    result_nils = Result(
        player = nils,
        game = game,
        points = 14
    )

    result_peer = Result(
        player = peer,
        game = game,
        points = -20
    )

    db.session.add(result_eric)
    db.session.add(result_lucas)
    db.session.add(result_nils)
    db.session.add(result_peer)

    db.session.commit()