# Generated by Django 3.2.9 on 2022-05-17 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0041_semester_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester_result',
            name='no_of_chanses',
        ),
    ]
