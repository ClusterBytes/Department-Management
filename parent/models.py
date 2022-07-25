from django.db import models
from student.models import profile_student

# Create your models here.
class parent_profile(models.Model):
    parent_id = models.CharField(primary_key=True, max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_no = models.BigIntegerField()
    email = models.EmailField(null=True)
    register_no = models.ForeignKey(profile_student, on_delete=models.CASCADE)
