from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from pointkeeper.extensions import db

from pointkeeper.models.game import Game
from pointkeeper.models.player import Player


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = db.Column(Integer, ForeignKey("games.id"), nullable=False)
    points = db.Column(Integer, nullable=False)

    game = relationship(Game)
    player = relationship(Player)

    def __repr__(self):
        return (
            f'Result(Player ID: {self.player_id}, '
            + f'Game ID: {self.game_id}, '
            + f'Points: {self.points})'
        )
