# Generated by Django 4.0.6 on 2023-02-08 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lobby.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='New Room', max_length=30)),
                ('code', models.CharField(default=lobby.models.generate_unique_code, max_length=8, unique=True)),
                ('about', models.TextField(max_length=200, null=True)),
                ('img', models.ImageField(default='lobby-img.png', upload_to='profile_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
