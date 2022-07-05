from django.contrib import admin
from django_restful_admin import admin as rest_admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as Old_UserAdmin
from directorio.models import User

# Register your models here.
class UserAdmin(Old_UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'adress', 'phone')
    
admin.site.register(User,UserAdmin)

rest_admin.site.register(User)
rest_admin.site.register(Group)