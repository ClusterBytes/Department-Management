# Generated by Django 3.2.9 on 2022-04-25 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hod", "0021_attendance_semester"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="internal_mark",
            name="exam_type",
        ),
        migrations.RemoveField(
            model_name="internal_mark",
            name="university_no",
        ),
        migrations.AddField(
            model_name="internal_mark",
            name="semester",
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="internal_mark",
            name="student_id",
            field=models.BigIntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="subject_to_staff",
            name="batch_id",
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name="subject_to_staff",
            name="semester",
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name="subject_to_staff",
            name="staff_id",
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name="subject_to_staff",
            name="subject_id",
            field=models.BigIntegerField(),
        ),
    ]
