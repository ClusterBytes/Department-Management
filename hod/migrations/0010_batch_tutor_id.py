# Generated by Django 3.2.9 on 2022-03-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hod", "0009_alter_subject_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="tutor_id",
            field=models.BigIntegerField(default=0),
        ),
    ]
