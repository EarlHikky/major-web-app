from datetime import datetime

from dateutil.relativedelta import relativedelta

from .utils import check_params


def create_params(period, value):
    today = datetime.now()
    current_year = today.year
    previous_year = today.year - 1
    current_quarter = (today.month - 1) // 3 + 1
    last_quarter = current_quarter - 1 if current_quarter > 1 else 4
    if today.month == 1:
        current_year = previous_year

    check_params(today, period, value)

    year_expr = {'sales__time_create__year': current_year}

    quarters = {
        'current': current_quarter,
        'previous': last_quarter,
    }

    months = {
        'current': today.month,
        'previous': (today - relativedelta(months=1)).month,
    }

    params_mapping = {
        ('year', 'current'): year_expr,
        ('year', 'previous'): {'sales__time_create__year': previous_year},
        ('quarter', 'current'): year_expr | {'sales__time_create__quarter': quarters['current']},
        ('quarter', 'previous'): year_expr | {'sales__time_create__quarter': quarters['previous']},
        ('month', 'current'): year_expr | {'sales__time_create__month': months['current']},
        ('month', 'previous'): year_expr | {'sales__time_create__month': months['previous']},
    }

    params = params_mapping.get((period, value), year_expr)

    return params