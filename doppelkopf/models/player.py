from sqlalchemy import (
    Column,
    Integer,
    Float,
    String
)

from doppelkopf.extensions import db

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    ranking = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    points_game_ration = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'Player(ID: {self.id}, Name: {self.name})'