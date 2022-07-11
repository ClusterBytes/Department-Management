# Generated by Django 3.2.9 on 2022-05-17 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hod", "0044_delete_semester_result"),
    ]

    operations = [
        migrations.CreateModel(
            name="semester_result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("university_no", models.CharField(max_length=255)),
                ("subject_id", models.BigIntegerField()),
                ("grade_point", models.BigIntegerField()),
                ("semester", models.BigIntegerField()),
                ("batch_id", models.BigIntegerField()),
                ("month", models.BigIntegerField()),
                ("year", models.BigIntegerField()),
            ],
        ),
    ]
