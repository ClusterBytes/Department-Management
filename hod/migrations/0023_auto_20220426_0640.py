# Generated by Django 3.2.9 on 2022-04-26 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hod", "0022_auto_20220425_2325"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="internal_mark",
            name="subject_code",
        ),
        migrations.AddField(
            model_name="internal_mark",
            name="subject_id",
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
