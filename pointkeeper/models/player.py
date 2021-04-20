from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from pointkeeper.extensions import db

from pointkeeper.models.community import Community


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    ranking = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    points_game_ration = db.Column(db.Float, default=0.0)
    community_id = db.Column(
        Integer,
        ForeignKey("communities.id"),
        nullable=False
    )
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    table = relationship(Community)

    def __repr__(self):
        return f'Player(ID: {self.id}, Name: {self.name})'
