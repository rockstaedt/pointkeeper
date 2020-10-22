from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    func,
    desc)
from sqlalchemy.orm import relationship
from datetime import datetime
from .extensions import db
from typing import Dict


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    ranking = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    points_game_ration = db.Column(db.Float, default=0.0)

    def update_game_statistics(self):
        self.total_points = Result.get_total_points_player(self.id)
        self.total_games = Result.get_total_games_player(self.id)
        if self.total_games != 0:
            self.points_game_ration = self.total_points/self.total_games
        player_id_to_rank_and_points = Result.get_total_points_all_ranked()
        if self.total_points != 0 or self.total_games != 0:
            self.ranking = player_id_to_rank_and_points[self.id]["ranking"]
        else:
            self.ranking = 999
            self.points_game_ration = 0

    def get_game_statistic_player(self) -> Dict:
        game_statistics = {
            "total_points": self.total_points,
            "total_games": self.total_games,
            "points_game_ration": round(self.points_game_ration, 2),
            "ranking": self.ranking
        }
        return game_statistics


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    played_matches = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Game('{self.id}', '{self.date}', '{self.played_matches}'"


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = db.Column(Integer, ForeignKey("games.id"), nullable=False)
    points = db.Column(Integer, nullable=False)

    game = relationship(Game)
    player = relationship(Player)

    @staticmethod
    def get_player_results(game_id: int):
        results = db.session.query(
            Result
        ).join(
            Game
        ).join(
            Player
        ).filter(
            Game.id == game_id
        ).all()
        player_name_to_points = {}
        for result in results:
            player_name_to_points[result.player.name] = result.points
        return player_name_to_points

    @staticmethod
    def get_total_points_all_ranked():
        results = db.session.query(
            Result.player_id,
            func.sum(Result.points).label("total_points_sum")
        ).group_by(
            Result.player_id
        ).order_by(
            desc("total_points_sum")
        ).all()
        player_id_to_rank_and_points= {}
        ranking = 1
        for result in results:
                player_id_to_rank_and_points[result.player_id] = {
                    "total_points": result.total_points_sum,
                    "ranking": ranking
                }
                ranking += 1
        return player_id_to_rank_and_points

    @staticmethod
    def get_total_points_player(player_id: int) -> int:
        results = db.session.query(
            Result.player_id,
            func.sum(Result.points).label("total_points_sum")
        ).filter(
            Result.player_id == player_id
        ).group_by(
            Result.player_id
        ).order_by(
            desc("total_points_sum")
        ).first()
        if results:
            return results.total_points_sum
        else:
            return 0

    @staticmethod
    def get_total_games_all() -> Dict:
        results = db.session.query(
            Result.player_id,
            func.sum(Game.played_matches).label("total_games_sum")
        ).join(
            Game
        ).group_by(
            Result.player_id
        ).all()
        player_id_to_total_games = {}
        for result in results:
                player_id_to_total_games[result.player_id] = result.total_games_sum
        return player_id_to_total_games

    @staticmethod
    def get_total_games_player(player_id) -> int:
        results = db.session.query(
            Result.player_id,
            func.sum(Game.played_matches).label("total_games_sum")
        ).join(
            Game
        ).filter(
            Result.player_id == player_id
        ).group_by(
            Result.player_id
        ).first()
        if results:
            return results.total_games_sum
        else:
            return 0