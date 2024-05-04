# Generated by Django 5.0.4 on 2024-04-30 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("league", "0002_match"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="goals_against",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="goals_for",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]