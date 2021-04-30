from sqlalchemy import func, extract

from pointkeeper.extensions import db

from pointkeeper.models import Game


def get_list_played_years() -> list:
    """
    This function returns a list of years in which games happened in ascending
    order.
    :return: List of years in ascending order.
    """
    result = db.session.query(
        func.min(extract('year', Game.date)).label('year_min'),
        func.max(extract('year', Game.date)).label('year_max')
    ).one()
    return list(range(int(result.year_max), int(result.year_min)-1, -1))
