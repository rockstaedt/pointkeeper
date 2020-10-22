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

    db.session.commit()