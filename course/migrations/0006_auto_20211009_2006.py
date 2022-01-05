# Generated by Django 3.2 on 2021-10-09 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapi', '0008_media'),
        ('course', '0005_auto_20211009_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='seminar',
            name='tags',
        ),
        migrations.AddField(
            model_name='seminar',
            name='starting_seminar',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='SeminarCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveBigIntegerField()),
                ('chapters', models.TextField(blank=True)),
                ('lessons', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('duration', models.PositiveBigIntegerField()),
                ('picture', models.ImageField(null=True, upload_to='')),
                ('seo', models.JSONField(blank=True, null=True)),
                ('capacity', models.PositiveSmallIntegerField()),
                ('starting_time', models.DateTimeField()),
                ('starting_seminar', models.DateField()),
                ('ending_time', models.DateTimeField()),
                ('city', models.CharField(max_length=140, null=True)),
                ('place', models.CharField(blank=True, max_length=300)),
                ('class_times', models.TextField()),
                ('attrib', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lapi.attrib')),
                ('copy_of', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copy', to='course.seminar')),
                ('prequel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sequel', to='course.seminarcopy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveBigIntegerField()),
                ('chapters', models.TextField(blank=True)),
                ('lessons', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('duration', models.PositiveBigIntegerField()),
                ('picture', models.ImageField(null=True, upload_to='')),
                ('seo', models.JSONField(blank=True, null=True)),
                ('days_after_exam', models.PositiveSmallIntegerField(null=True)),
                ('after_days_exam', models.PositiveSmallIntegerField(null=True)),
                ('attrib', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lapi.attrib')),
                ('copy_of', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('prequel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sequel', to='course.coursecopy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
