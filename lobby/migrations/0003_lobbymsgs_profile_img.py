# Generated by Django 4.0.6 on 2023-02-08 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_lobbymsgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbymsgs',
            name='profile_img',
            field=models.ImageField(default='lobby-img.png', upload_to='text_profiles'),
        ),
    ]
