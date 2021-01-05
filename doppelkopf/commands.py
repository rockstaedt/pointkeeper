import click
from flask.cli import with_appcontext

from .extensions import db
from doppelkopf.models import Player
from doppelkopf.models import Table

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

    eric = Player(
        name = "Eric",
        table_id = 1,
        image_file = 'Eric.png'
    )
    lucas = Player(
        name = "Lucas",
        table_id = 1,
        image_file = 'Lucas.png'
    )
    marco = Player(
        name = "Marco",
        table_id = 1,
        image_file = 'Marco.png'
    )
    nils = Player(
        name = "Nils",
        table_id = 1,
        image_file = 'Nils.png'
    )
    peer = Player(
        name = "Peer",
        table_id = 1,
        image_file = 'Peer.png'
    )

    db.session.add(eric)
    db.session.add(lucas)
    db.session.add(marco)
    db.session.add(nils)
    db.session.add(peer)

    table = Table(
        name = "Cooking Like OG",
        pin = "1234"
    )

    db.session.add(table)

    db.session.commit()