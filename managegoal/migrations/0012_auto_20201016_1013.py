# Generated by Django 3.1 on 2020-10-16 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managegoal', '0011_auto_20201011_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='lon',
            field=models.FloatField(null=True),
        ),
    ]