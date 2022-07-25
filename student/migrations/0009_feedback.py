# Generated by Django 3.2.9 on 2022-07-17 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0051_auto_20220618_1715'),
        ('student', '0008_auto_20220618_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_id', models.BigIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('subject_staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hod.subject_to_staff')),
            ],
        ),
    ]
