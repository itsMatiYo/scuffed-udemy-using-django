# Generated by Django 3.2 on 2021-10-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='init_price',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='coursecopy',
            name='init_price',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='seminar',
            name='init_price',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='seminarcopy',
            name='init_price',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
