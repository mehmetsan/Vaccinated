# Generated by Django 5.0.6 on 2024-06-10 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_uservaccination_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="role",
            field=models.CharField(
                choices=[("admin", "Admin"), ("normal", "Normal")],
                default="normal",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="uservaccination",
            name="vaccination",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.vaccination",
            ),
        ),
        migrations.AlterField(
            model_name="uservaccination",
            name="yearly_vaccination",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.yearlyvaccination",
            ),
        ),
        migrations.CreateModel(
            name="TwoFactorEmailModel",
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
                ("code", models.CharField(max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expiration", models.DateTimeField(default=None, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.appuser"
                    ),
                ),
            ],
        ),
    ]
