# Generated by Django 4.0.6 on 2023-02-11 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0005_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='no_of_members',
            field=models.IntegerField(default=0),
        ),
    ]
