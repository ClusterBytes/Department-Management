# Generated by Django 4.0 on 2022-01-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0002_alter_profile_student_university_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile_student",
            name="photo",
            field=models.ImageField(
                default="images/user_default_image.png", null=True, upload_to="images/"
            ),
        ),
    ]
