# Generated by Django 4.1.7 on 2023-03-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_course_ccode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='ccode',
            field=models.CharField(max_length=200),
        ),
    ]