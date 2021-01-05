from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from doppelkopf.extensions import db

from doppelkopf.models.table import Table

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    ranking = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    points_game_ration = db.Column(db.Float, default=0.0)
    table_id = db.Column(Integer, ForeignKey("tables.id"), nullable=False)

    table = relationship(Table)

    def __repr__(self):
        return f'Player(ID: {self.id}, Name: {self.name})'