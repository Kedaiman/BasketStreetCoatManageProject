# Generated by Django 3.1 on 2020-10-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managegoal', '0010_auto_20201011_0613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='changeapplication',
            old_name='changedvariable',
            new_name='changevariable',
        ),
        migrations.RenameField(
            model_name='changedhistory',
            old_name='changedvariable',
            new_name='changevariable',
        ),
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=models.CharField(max_length=10),
        ),
    ]