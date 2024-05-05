# Generated by Django 5.0.4 on 2024-05-04 08:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("matches", "0009_alter_match_away_score_alter_match_home_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="away_score",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Score Équipe Extérieur",
            ),
        ),
        migrations.AlterField(
            model_name="match",
            name="home_score",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Score Équipe Domicile",
            ),
        ),
    ]
