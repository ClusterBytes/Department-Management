# Generated by Django 3.2.9 on 2022-05-17 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0042_remove_semester_result_no_of_chanses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester_result',
            old_name='scheme',
            new_name='batch_id',
        ),
    ]
