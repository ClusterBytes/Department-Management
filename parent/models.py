from django.db import models
from student.models import profile_student

# Create your models here.
class parent_profile(models.Model):
    parent_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_no = models.BigIntegerField()
    email = models.EmailField()
    register_no = models.ForeignKey(profile_student, on_delete=models.CASCADE)
