# Generated by Django 4.0.5 on 2022-07-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parent', '0002_auto_20220712_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent_profile',
            name='parent_id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]