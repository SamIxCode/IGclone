# Generated by Django 4.1.5 on 2023-02-01 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("baseapp", "0002_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="username",
            field=models.CharField(default="null", max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 2, 1, 16, 33, 18, 370294, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
