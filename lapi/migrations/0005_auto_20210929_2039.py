# Generated by Django 3.2 on 2021-09-29 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lapi', '0004_ticket4adviser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket4adviser',
            options={'ordering': ['-bought_at']},
        ),
        migrations.RemoveField(
            model_name='category',
            name='advisers',
        ),
    ]
