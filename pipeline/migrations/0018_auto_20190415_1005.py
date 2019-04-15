# Generated by Django 2.2 on 2019-04-15 08:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pipeline", "0017_auto_20190414_1452")]

    operations = [
        migrations.AddField(
            model_name="videoformat",
            name="duration_millis",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="videoformat",
            name="file_size",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="videoformat",
            name="frame_rate",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]