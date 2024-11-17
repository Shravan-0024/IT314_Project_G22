# Generated by Django 5.1.2 on 2024-11-16 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_home", "0003_feedback"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="app_recommend",
            field=models.CharField(
                blank=True,
                choices=[
                    ("yes", "👍 Yes, I would recommend this app"),
                    ("no", "👎 No, I would not recommend it"),
                    ("maybe", "🤔 Maybe, I might recommend it"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="app_usability",
            field=models.CharField(
                blank=True,
                choices=[
                    ("easy", "✅ Yes, the site was easy to use"),
                    ("difficult", "❌ No, the site was difficult to use"),
                    ("average", "😐 It was average"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="helpful_info",
            field=models.CharField(
                blank=True,
                choices=[
                    ("helpful", "👍 Yes, it was very helpful!"),
                    ("not_helpful", "👎 No, it wasn’t helpful."),
                    ("partially_helpful", "🤔 It was somewhat helpful."),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="predictions_accuracy",
            field=models.CharField(
                blank=True,
                choices=[
                    ("accurate", "🎯 Yes, the predictions were accurate"),
                    ("inaccurate", "❌ No, the predictions were inaccurate"),
                    ("not_sure", "🤷 Not sure"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="user_interface",
            field=models.CharField(
                blank=True,
                choices=[
                    ("intuitive", "👌 Yes, the interface was intuitive"),
                    ("confusing", "😕 No, the interface was confusing"),
                    ("okay", "🙂 It was okay"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Fav_loc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("favourite_location", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]