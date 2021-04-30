from sqlalchemy import func, extract

from pointkeeper.extensions import db

from pointkeeper.models import Game


def get_list_played_years(desc: bool = True) -> list:
    """
    This function returns a list of years in which games happened in descending
    order if not specified otherwise.

    :param desc: Specifies the ordering of the list.
    :return: List of years.
    """
    result = db.session.query(
        func.min(extract('year', Game.date)).label('year_min'),
        func.max(extract('year', Game.date)).label('year_max')
    ).one()
    if desc:
        return list(range(int(result.year_max), int(result.year_min)-1, -1))
    else:
        return list(range(int(result.year_min), int(result.year_max) + 1))
