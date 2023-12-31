# Generated by Django 4.1.7 on 2023-03-18 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0002_remove_modules_course_remove_question_modules_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=200)),
                ('dept', models.CharField(max_length=200)),
                ('sem', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_no', models.CharField(max_length=200)),
                ('mname', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('marks', models.CharField(max_length=200)),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=200)),
                ('rbt_level', models.CharField(choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')], max_length=200)),
                ('modules', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.module')),
            ],
        ),
    ]
