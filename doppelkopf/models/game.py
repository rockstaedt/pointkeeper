from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from datetime import datetime

from doppelkopf.extensions import db

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    played_matches = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Game('{self.id}', '{self.date}', '{self.played_matches}')"