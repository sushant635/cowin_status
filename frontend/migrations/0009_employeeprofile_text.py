# Generated by Django 3.2.6 on 2021-09-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_alter_employeeprofile_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]