# Generated by Django 3.2.9 on 2022-03-20 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hod", "0013_subject_to_staff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subject_to_staff",
            old_name="code",
            new_name="subject_id",
        ),
        migrations.RemoveField(
            model_name="subject_to_staff",
            name="scheme",
        ),
        migrations.RemoveField(
            model_name="subject_to_staff",
            name="semester",
        ),
    ]
