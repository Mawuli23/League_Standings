# Generated by Django 5.0.4 on 2024-05-12 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("matches", "0002_alter_team_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamLeague",
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
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matches.league"
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matches.team"
                    ),
                ),
            ],
        ),
    ]