# Generated by Django 3.2.9 on 2022-07-17 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_rename_subject_staff_feedback_subject_to_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='feedback_id',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.profile_student'),
        ),
    ]
