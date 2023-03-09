from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Account
from django.utils.html import format_html

# for costomising the passwords in the admin panel


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','username','last_login','date_joined','is_active')
    readonly_fields=('last_login','date_joined')
    ordering=("date_joined",)
    
    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)