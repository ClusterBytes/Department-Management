from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class MyUserManager(BaseUserManager):
    def create_user(self, username,first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            #username=self.normalize_email(email),
            #date_of_birth=date_of_birth,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            #date_of_birth=date_of_birth,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    #date_of_birth = models.DateField()
    first_name =  models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_faculty= models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

from django.contrib.auth.backends import BaseBackend
from .models import MyUser
#from IntellerMatrix.CommonUtilities.constants import Constants


class AuthenticationBackend(BaseBackend):
    """
    Authentication Backend
    :To manage the authentication process of user
    """

    def authenticate(self, request, username=None, password=None, is_hod=None, is_faculty=None, is_student=None):
        print("pass",password)
        try:
            user = MyUser.objects.get(username=username, is_hod=is_hod, is_faculty=is_faculty, is_student=is_student)
        except MyUser.DoesNotExist:
            return None
        if user is not None and user.check_password(password):
            if user.is_active == True:
                return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

'''class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        category = ''
        if self.is_staff :
            category = 'Staff'
        elif self.is_hod:
            category = 'HOD'
        elif self.is_student:
            category = 'Student'
        name = self.first_name +" "+ self.last_name + " - " + category
        return name'''

'''class User(AbstractBaseUser):
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
'''    
    



