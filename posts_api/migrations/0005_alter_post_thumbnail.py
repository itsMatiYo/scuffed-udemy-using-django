# Generated by Django 3.2 on 2021-10-09 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_api', '0004_auto_20211009_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
