from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import LoginUserForm
from .views import StaffAPIView, SalesAPIView, StaffView, AddStaffView, AddSellView, \
    test_view, logout_view, WebAppView, RatingView, StaffDetailView

urlpatterns = [
    path('', StaffView.as_view(), name='home'),
    path('api/v1/sales-list/', SalesAPIView.as_view()),
    path('api/v1/staff-list/', StaffAPIView.as_view()),
    path('api/v1/staff-list/<int:pk>/', StaffAPIView.as_view()),
    path('add-staff/', AddStaffView.as_view(), name='add_staff'),
    path('add-sell/', AddSellView.as_view(), name='add_sell'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('sales-by-fio/<slug:slug>/', StaffDetailView.as_view(), name='sales_by_fio'),
    path('rating/<slug:period>/<slug:value>/', RatingView.as_view(), name='rating'),
    path('test/', test_view, name='test'),
    path('web-app/', WebAppView.as_view(), name='web_app'),
    path('login/',
         auth_views.LoginView.as_view(template_name='kpi/login.html', form_class=LoginUserForm),
         name='login'),
    path('logout/', logout_view, name='logout'),

]
