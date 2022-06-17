from django.contrib import admin

# Register your models here.
from student.models import profile_student

# Register your models here.


@admin.register(profile_student)
class profile_studentAdmin(admin.ModelAdmin):
    pass
