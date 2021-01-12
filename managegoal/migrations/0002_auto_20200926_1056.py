# Generated by Django 3.1 on 2020-09-26 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageuser', '0001_initial'),
        ('managegoal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='impression',
            name='good_users',
            field=models.ManyToManyField(related_name='good_users', to='manageuser.User'),
        ),
        migrations.AlterField(
            model_name='impression',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='manageuser.user'),
        ),
    ]