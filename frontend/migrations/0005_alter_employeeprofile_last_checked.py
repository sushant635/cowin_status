# Generated by Django 3.2.6 on 2021-09-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20210909_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='last_checked',
            field=models.DateField(blank=True, null=True),
        ),
    ]
