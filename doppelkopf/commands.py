import click
from flask.cli import with_appcontext

from .extensions import db
from doppelkopf.models import Player

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

    db.session.commit()