from email.policy import default
from django.db import models


# Create your models here.
class profile(models.Model):
    Faculty_unique_id = models.CharField(max_length=255)
    Profile_photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')
    First_name = models.CharField(max_length=255, null=False)
    Last_name = models.CharField(max_length=255, null=True)
    Gender = models.CharField(max_length=255, null=True, choices=[('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others')])
    Date_of_Birth = models.DateField(null=True)
    Aadhar_No = models.BigIntegerField(null=True)
    Caste = models.CharField(max_length=255, null=True)
    Religion = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    PAN = models.CharField(max_length=25, null=True)
    Date_of_Joining = models.DateField(null=True)
    AICTE_unique_Id = models.CharField(max_length=255, null=True)
    Appointment_type = models.CharField(max_length=255, null=True)
    Cadre = models.CharField(max_length=255, null=True)
    Designation = models.CharField(max_length=255, null=True)
    Specialisation = models.CharField(max_length=250, null=True)
    Department_of_program = models.CharField(max_length=250, null=True)
    Examiner_institution = models.CharField(max_length=250, null=True)
    Area_of_Research = models.CharField(max_length=250, null=True)
    email = models.EmailField(null=True)
    phone_no = models.BigIntegerField(null=True)
    
    
    def __str__(self):
        name = self.First_name +" "+ self.Last_name
        return name
        
    

    