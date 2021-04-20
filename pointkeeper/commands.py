import click
from flask.cli import with_appcontext

from .extensions import db
from pointkeeper.models import Player
from pointkeeper.models import Community


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

    eric = Player(
        name="Eric",
        community_id=1,
        image_file='Eric.png'
    )
    lucas = Player(
        name="Lucas",
        community_id=1,
        image_file='Lucas.png'
    )
    marco = Player(
        name="Marco",
        community_id=1,
        image_file='Marco.png'
    )
    nils = Player(
        name="Nils",
        community_id=1,
        image_file='Nils.png'
    )
    peer = Player(
        name="Peer",
        community_id=1,
        image_file='Peer.png'
    )

    db.session.add(eric)
    db.session.add(lucas)
    db.session.add(marco)
    db.session.add(nils)
    db.session.add(peer)

    table = Community(
        name="Cooking Like OG",
        pin="1234"
    )

    db.session.add(table)

    db.session.commit()
