# Generated by Django 4.1.7 on 2023-03-18 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modules',
            name='course',
        ),
        migrations.RemoveField(
            model_name='question',
            name='modules',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Modules',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]