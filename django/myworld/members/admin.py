from django.contrib import admin
from .models import Category,Article,Question

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Extend_User

class EmployeeInline(admin.StackedInline):
    model = Extend_User
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Extend_User)