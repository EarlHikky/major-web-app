from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import Staff, Sales, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name', 'get_html_photo')
    prepopulated_fields = {'slug': ('name',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')

    get_html_photo.short_description = "Фото"


class SalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'time_create', 'total')
    list_display_links = ('id', 'fio')
    search_fields = ('fio', 'content')
    list_filter = ('fio', 'time_create')


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Staff, StaffAdmin)
admin.site.register(Sales, SalesAdmin)

admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'
