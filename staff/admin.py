from django.contrib import admin

# Register your models here.
from staff.models import profile

# Register your models here.


@admin.register(profile)
class profileAdmin(admin.ModelAdmin):
    pass
