# Generated by Django 4.0.6 on 2023-02-08 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0003_lobbymsgs_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbymsgs',
            name='name',
            field=models.CharField(default='user', max_length=30),
        ),
    ]
