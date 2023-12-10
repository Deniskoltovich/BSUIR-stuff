from django.contrib import admin

from .models import UserGroup, Employee, Activity, Admin

admin.site.register(UserGroup)
admin.site.register(Employee)
admin.site.register(Activity)
admin.site.register(Admin)

