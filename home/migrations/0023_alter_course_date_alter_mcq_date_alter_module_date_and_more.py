# Generated by Django 4.1.7 on 2023-03-29 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_course_date_mcq_date_module_date_question_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='mcq',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='module',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='date'),
        ),
    ]
