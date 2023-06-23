from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.http import Http404


def check_params(today, period, value):
    valid_values = ('current', 'previous')
    valid_periods = {'year': range(2000, today.year + 1),
                     'quarter': (1, 2, 3, 4),
                     'month': range(1, 13)}
    try:
        value = int(value)
    except ValueError:
        if value not in valid_values:
            raise Http404("Неверно указаны параметры поиска.")
    else:
        if value not in valid_periods.get(period, {}):
            raise Http404("Неверно указаны параметры поиска.")
        return period, value


def create_params(period, value):
    today = datetime.now()
    current_year = today.year
    previous_year = today.year - 1
    if today.month == 1:
        current_year = previous_year
    current_quarter = (today.month - 1) // 3 + 1
    previous_quarter = current_quarter - 1 if current_quarter > 1 else 4
    current_month = today.month
    previous_month = (today - relativedelta(months=1)).month

    check_params(today, period, value)
    params_mapping = {
        'year': {
            'current': {'sales__time_create__year': current_year},
            'previous': {'sales__time_create__year': previous_year},

        },
        'quarter': {
            'current': {'sales__time_create__year': current_year,
                        'sales__time_create__quarter': current_quarter},
            'previous': {'sales__time_create__year': current_year,
                         'sales__time_create__quarter': previous_quarter},

        },
        'month': {
            'current': {'sales__time_create__year': current_year,
                        'sales__time_create__month': current_month},
            'previous': {'sales__time_create__year': current_year,
                         'sales__time_create__month': previous_month},

        }
    }
    filter_params = params_mapping.get(period).get(value, {'sales__time_create__year': current_year,
                                                           f'sales__time_create__{period}': value})
    return filter_params


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user = self.request.user
        auth = user.is_authenticated
        if auth:
            profile = user.profile
            context['auth'] = auth
            context['photo'] = profile.photo
            context['username'] = user.username
        return context
