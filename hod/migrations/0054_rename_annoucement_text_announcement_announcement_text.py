# Generated by Django 3.2.9 on 2022-07-25 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0053_announcement_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='annoucement_text',
            new_name='announcement_text',
        ),
    ]
