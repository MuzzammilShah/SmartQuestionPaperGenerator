# Generated by Django 4.1.7 on 2023-03-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_mcq_marks_alter_question_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='modno',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=200),
        ),
    ]