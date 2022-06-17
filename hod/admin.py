from django.contrib import admin

from hod.models import batch, scheme, subject, subject_to_staff

# Register your models here.
@admin.register(batch)
class Batches(admin.ModelAdmin):
    pass

@admin.register(subject)
class Subject(admin.ModelAdmin):
    pass

@admin.register(scheme)
class Scheme(admin.ModelAdmin):
    pass

@admin.register(subject_to_staff)
class Scheme(admin.ModelAdmin):
    pass