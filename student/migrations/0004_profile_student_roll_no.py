# Generated by Django 3.2.9 on 2022-04-24 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0003_alter_profile_student_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile_student",
            name="roll_no",
            field=models.BigIntegerField(null=True),
        ),
    ]
