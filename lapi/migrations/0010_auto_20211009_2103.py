# Generated by Django 3.2 on 2021-10-09 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_api', '0005_alter_post_thumbnail'),
        ('users', '0005_auto_20210929_2046'),
        ('course', '0006_auto_20211009_2006'),
        ('lapi', '0009_auto_20211009_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='posts_api.post'),
        ),
        migrations.CreateModel(
            name='Ticket4Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ticket4teacher', to='users.student')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='course.course')),
            ],
        ),
    ]