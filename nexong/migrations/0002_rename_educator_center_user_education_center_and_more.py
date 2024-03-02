# Generated by Django 5.0.2 on 2024-03-02 10:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nexong", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="educator_center",
            new_name="education_center",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_admin",
        ),
        migrations.AlterField(
            model_name="donation",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("ANNUAL", "Anual"),
                    ("MONTHLY", "Mensual"),
                    ("QUARTERLY", "Trimestral"),
                    ("SIX-MONTHLY", "Seis Meses"),
                ],
                default="MONTHLY",
                max_length=11,
            ),
        ),
        migrations.AlterField(
            model_name="volunteer",
            name="postal_code",
            field=models.IntegerField(
                default=10000,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(90000),
                ],
            ),
        ),
    ]