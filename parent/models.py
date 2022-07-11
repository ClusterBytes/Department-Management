from django.db import models
from student.models import profile_student

# Create your models here.
class parent_profile(models.Model):
    parent_id = models.BigIntegerField(primary_key=True)
    phone_no = models.BigIntegerField()
    email = models.EmailField()

class parent_student(models.Model):
    register_no = models.ForeignKey(profile_student,on_delete=models.CASCADE)