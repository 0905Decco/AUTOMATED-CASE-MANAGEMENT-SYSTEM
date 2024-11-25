from django.contrib import admin
from .models import Litigant, Judge, Case, Admin,UserType

admin.site.register(Litigant)
admin.site.register(Judge)
admin.site.register(Case)
admin.site.register(Admin)
admin.site.register(UserType)