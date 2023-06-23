import locale

from PIL import Image
from _decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify

locale.setlocale(locale.LC_ALL, "ru_RU")
tz = timezone.get_default_timezone()


def get_upload_path(instance, filename):
    name = instance.slug
    return f'photos/{name}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='photos/')


class Staff(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='ФИО')
    photo = models.ImageField(upload_to=get_upload_path, blank=True, verbose_name='Фото')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('staff')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo)
            img = img.resize((200, 200))
            img.save(self.photo.path, format='PNG')

    @property
    def surname(self):
        return self.name.split()[0]

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']


class Sales(models.Model):
    fio = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, verbose_name='ФИО', related_name='sales')
    extradition = models.IntegerField(verbose_name='Выдачи', blank=True, default=0, validators=[MinValueValidator(0)])
    ti = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ТИ', blank=True, default=0.0)
    kis = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='КИС', blank=True, default=0.0)
    trener = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Тренер', blank=True, default=0.0)
    client = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Клиент', blank=True, default=0.0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name='Итого')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total = float(
            sum(map(Decimal, [self.extradition, self.ti, self.kis, self.trener, self.client])).quantize(Decimal("1.0")))
        super(Sales, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sales_by_fio', kwargs={'slug': self.fio.slug})

    def __str__(self):
        return f'Продажа {self.fio} от {self.time_create.strftime("%d/%b/%Y, %H:%M:%S")}'

    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'
        ordering = ['-time_create', 'fio']
