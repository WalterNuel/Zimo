# Generated by Django 4.0.6 on 2022-11-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_first',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='author_img',
            field=models.ImageField(blank=True, upload_to='post_author_images'),
        ),
        migrations.AddField(
            model_name='post',
            name='author_last',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]