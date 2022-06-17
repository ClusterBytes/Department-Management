import email
from django.db import models


# Create your models here.
class profile_student(models.Model):
    register_no = models.CharField(max_length=255)
    university_no = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    roll_no = models.BigIntegerField(unique=False, null=True)
    branch = models.CharField(max_length=255, null=True)
    aadhar_no = models.BigIntegerField(unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_no = models.BigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    sex = models.CharField(max_length=10, null=True, choices=[('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others')])
    date_of_birth = models.DateField(unique=False, null=True)
    nationality = models.CharField(max_length=255, null=True)
    religion = models.CharField(max_length=255, null=True)
    caste = models.CharField(max_length=255, null=True)
    native_place = models.CharField(max_length=255, null=True)
    batch = models.BigIntegerField(unique=False, null=False)
    scheme_id = models.BigIntegerField(unique=False, null=False)


    blood_groups = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=10, choices=blood_groups, null=True)
    hobbies = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')
    sign = models.ImageField(upload_to='images/', null=True)

    
    

    def __str__(self):
        name = self.first_name +" "+ self.last_name
        return name

class qualifications(models.Model):
    s_id = models.BigIntegerField(null=False)
    name_of_exam = models.CharField(max_length=256, null=True)
    name_of_institution = models.CharField(max_length=256, null=True)
    month = models.BigIntegerField(null=True)
    year = models.BigIntegerField(null=True)
    mark = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    no_of_chances = models.BigIntegerField(null=True)

class parents(models.Model):
    s_id = models.BigIntegerField(null=False)
    fathers_name = models.CharField(max_length=256,null=True)
    fathers_occupation = models.CharField(max_length=256,null=True)
    mothers_name = models.CharField(max_length=256,null=True)
    mothers_occupation = models.CharField(max_length=256,null=True)
    address = models.CharField(max_length=256,null=True)
    res_address = models.CharField(max_length=256,null=True)
    official_address = models.CharField(max_length=256,null=True)
    fathers_email_id = models.EmailField(null=True)
    mothers_email_id = models.EmailField(null=True)
    fathers_number = models.BigIntegerField(null=True)
    mothers_number = models.BigIntegerField(null=True)
