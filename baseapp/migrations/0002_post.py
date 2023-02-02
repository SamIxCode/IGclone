# Generated by Django 4.1.5 on 2023-01-24 21:56

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("baseapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("id_user", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="post_pisctures")),
                ("caption", models.TextField()),
                (
                    "created_at",
                    models.DateTimeField(
                        verbose_name=datetime.datetime(2023, 1, 24, 21, 56, 28, 970988)
                    ),
                ),
                ("likes", models.IntegerField(default=0)),
            ],
        ),
    ]
