# Generated by Django 4.1.7 on 2023-03-20 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0004_alter_course_dept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]