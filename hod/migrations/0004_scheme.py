# Generated by Django 4.0 on 2021-12-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0003_subject_delete_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='scheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(max_length=255)),
            ],
        ),
    ]
