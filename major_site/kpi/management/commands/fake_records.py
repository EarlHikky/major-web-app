import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from kpi.models import Staff, Sales


class Command(BaseCommand):
    help = 'create records'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, default=1, help='Number of records to create')
        parser.add_argument('--years', type=int, default=3, help='Number of years to consider')

    def handle(self, *args, **options):
        amount = int(options['amount'])
        years = int(options['years'])
        fake = Faker()

        # Get all Staff objects
        staff_members = Staff.objects.all()

        # Get all User objects
        users = User.objects.all()

        # Loop to create Sales objects
        for i in range(amount):
            # Get random Staff object
            staff = fake.random_element(staff_members)

            # Generate random date within the last few years
            start_date = timezone.now() - datetime.timedelta(days=365 * years)
            end_date = timezone.now()
            time_create = fake.date_time_between(start_date=start_date, end_date=end_date,
                                                 tzinfo=timezone.get_current_timezone())

            # Create Sales object
            sale = Sales.objects.create(
                fio=staff,
                extradition=fake.random_int(min=0, max=10),
                ti=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
                kis=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
                trener=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
                client=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
                total=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
                time_create=time_create,
                user=fake.random_element(users)
            )

            # Save the Sales object
            sale.save()

        print('Done.')
