# Generated by Django 4.1.2 on 2022-10-19 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_avatar_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('postimage', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('auther', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked', models.ManyToManyField(default=None, related_name='liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
