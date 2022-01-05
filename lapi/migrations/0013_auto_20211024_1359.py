# Generated by Django 3.2 on 2021-10-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapi', '0012_companyinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='alt',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='media',
            name='seo',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]