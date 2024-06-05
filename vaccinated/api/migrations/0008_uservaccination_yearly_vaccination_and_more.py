# Generated by Django 5.0.6 on 2024-06-05 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_yearlyvaccination_remove_vaccination_yearly"),
    ]

    operations = [
        migrations.AddField(
            model_name="uservaccination",
            name="yearly_vaccination",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.yearlyvaccination",
            ),
        ),
        migrations.AlterField(
            model_name="uservaccination",
            name="vaccination",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.vaccination",
            ),
        ),
    ]
