# Generated by Django 3.2 on 2021-10-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20211016_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2048)),
                ('url', models.URLField()),
            ],
        ),
    ]
