from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView
from rest_framework import generics

from .forms import AddStaffForm, AddSellForm
from .models import Staff, Sales
from .serializers import StaffSerializer, SalesSerializer
from .utils import create_params, DataMixin


class SalesAPIView(generics.CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class StaffAPIView(generics.ListAPIView):
    serializer_class = StaffSerializer

    def get_queryset(self):
        """This view should return a staff by id"""
        if self.kwargs.get('pk', None):
            pk = self.kwargs['pk']
            return Staff.objects.filter(pk=pk)
        return Staff.objects.all()


class AddStaffView(DataMixin, PermissionRequiredMixin, CreateView):
    model = Staff
    form_class = AddStaffForm
    template_name = 'kpi/add_staff.html'
    permission_required = 'kpi.add_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title='Добавить сотрудника'))
        return context


class AddSellView(DataMixin, PermissionRequiredMixin, CreateView):
    model = Sales
    form_class = AddSellForm
    template_name = 'kpi/add_sell.html'
    permission_required = 'kpi.add_sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title='Добавить продажу'))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WebAppView(DataMixin, PermissionRequiredMixin, CreateView):
    model = Sales
    form_class = AddSellForm
    template_name = 'kpi/web_app.html'
    permission_required = 'kpi.add_sales'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StaffView(DataMixin, ListView):
    model = Staff
    template_name = 'kpi/staff.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title='Сотрудники'))
        return context


class RatingView(DataMixin, View):
    CACHE_TIME = 60 * 15

    def get(self, request, period, value):
        filter_params = create_params(period, value)

        employees = cache.get(f'records_{period}_{value}')
        if not employees:
            employees = Staff.objects.filter(**filter_params).annotate(
                total_sales=Sum('sales__total'),
                extradition_sum=Sum('sales__extradition'),
                ti_sum=Sum('sales__ti'),
                kis_sum=Sum('sales__kis'),
                trener_sum=Sum('sales__trener'),
                client_sum=Sum('sales__client'),
            )
            cache.set(f'records_{period}_{value}', employees, self.CACHE_TIME)

        if not employees:
            raise Http404("Не найдено продаж с указанными параметрами.")

        records = []
        for employee in employees:
            record = {
                'fio': employee,
                'total': employee.total_sales,
                'extradition': employee.extradition_sum,
                'ti': employee.ti_sum,
                'kis': employee.kis_sum,
                'trener': employee.trener_sum,
                'client': employee.client_sum,
            }
            records.append(record)
        sorted_records = sorted(records, key=lambda x: x.get('total', 0), reverse=True)
        context = {'title': 'Рейтинг',
                   'records': sorted_records,
                   'positions': (
                       (0, 'Первое место'),
                       (1, 'Второе место'),
                       (2, 'Третье место'),)}
        context.update(self.get_user_context())
        return render(request, 'kpi/rating.html', context)


class StaffDetailView(DataMixin, View):
    def get(self, request, slug):
        fio = get_object_or_404(Staff, slug=slug)
        sales = Sales.objects.filter(fio=fio)
        context = {'sales': sales,
                   'fio': fio,
                   'categories': ('Дата', 'Выдачи', 'ТИ', 'КИС',
                                  'Тренер', 'Клиент', 'Итого')
                   }
        context.update(self.get_user_context())
        return render(request, 'kpi/staff_detail.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def test_view(request):
    context = {}
    auth = request.user.is_authenticated
    user = request.user
    profile = user.profile
    if auth:
        context['auth'] = auth
        context['photo'] = profile.photo
        context['username'] = user.username

    return render(request, 'kpi/test.html', {'context': context})
