# Generated by Django 3.2.9 on 2022-07-17 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_auto_20220717_1038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='student_id',
            new_name='student',
        ),
    ]