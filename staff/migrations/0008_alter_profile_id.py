# Generated by Django 3.2.9 on 2022-06-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0007_auto_20220616_1819"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
