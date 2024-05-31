from django.contrib import admin

from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre',  'email','is_staff','is_superuser','is_active', )
    list_display_links = ('nombre',  'email','is_staff','is_superuser','is_active', )
    search_fields = ('nombre',  'email','is_staff','is_superuser','is_active', )
    list_per_page = 25

admin.site.register(User, UserAdmin)