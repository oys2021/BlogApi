from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import CustomUser

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     fieldsets = UserAdmin.fieldsets + (
#         ('Custom Fields', {'fields': ('bio', 'profile_image')}),
#     )
#     list_display = ['username', 'email', 'is_staff']
admin.site.register(CustomUser)