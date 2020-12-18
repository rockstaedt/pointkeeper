from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from typing import Dict

from doppelkopf.extensions import db

from doppelkopf.models.game import Game
from doppelkopf.models.player import Player

class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = db.Column(Integer, ForeignKey("games.id"), nullable=False)
    points = db.Column(Integer, nullable=False)

    game = relationship(Game)
    player = relationship(Player)