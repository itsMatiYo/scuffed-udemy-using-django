# Generated by Django 3.2 on 2021-10-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210929_2046'),
        ('posts_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(to='users.Student'),
        ),
    ]
