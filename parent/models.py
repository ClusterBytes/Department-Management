from django.db import models
from student.models import profile_student

# Create your models here.
class parent_profile(models.Model):
    parent_id = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone_no = models.BigIntegerField()
    email = models.EmailField()

class parent_student(models.Models):
    register_no = models.ForeignKey(profile_student)