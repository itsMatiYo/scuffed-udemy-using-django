# Generated by Django 3.2 on 2021-10-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20211016_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='days_after_exam',
        ),
        migrations.AddField(
            model_name='answerfile',
            name='changed_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]