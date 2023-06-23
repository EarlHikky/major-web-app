from django.test import TestCase
from django.urls import reverse
from .models import Staff, Sales


class SalesModelTestCase(TestCase):
    def test_create_sales_with_valid_data(self):
        staff = Staff.objects.create(name='John Doe')
        sales = Sales.objects.create(
            fio=staff,
            extradition=10,
            ti=20.5,
            kis=15.3,
            trener=5.75,
            client=12.25,
            user_id=1
        )
        self.assertIsNotNone(sales.pk)

    def test_create_sales_with_invalid_data(self):
        staff = Staff.objects.create(name='John Doe')
        with self.assertRaises(Exception):
            sales = Sales.objects.create(
                fio=staff,
                extradition=-10,
                ti=20.5,
                kis=15.3,
                trener=5.75,
                client=12.25,
                user_id=1
            )

    def test_calculate_sales_total(self):
        staff = Staff.objects.create(name='John Doe')
        sales = Sales.objects.create(
            fio=staff,
            extradition=10,
            ti=20.5,
            kis=15.3,
            trener=5.76,
            client=12.25,
            user_id=1
        )
        expected_total = 10 + 20.5 + 15.3 + 5.75 + 12.25
        self.assertEqual(sales.total, expected_total)

    def test_get_absolute_url(self):
        staff = Staff.objects.create(name='John Doe')
        sales = Sales.objects.create(
            fio=staff,
            extradition=10,
            ti=20.5,
            kis=15.3,
            trener=5.75,
            client=12.25,
            user_id=1
        )
        expected_url = reverse('sales_by_fio', kwargs={'slug': staff.slug})
        self.assertEqual(sales.get_absolute_url(), expected_url)
