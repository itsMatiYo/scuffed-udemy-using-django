# Generated by Django 3.2 on 2021-10-02 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lapi', '0005_auto_20210929_2039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='tag',
            new_name='tags',
        ),
    ]
