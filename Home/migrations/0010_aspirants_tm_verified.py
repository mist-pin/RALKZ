# Generated by Django 4.2.11 on 2024-04-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_aspirants_aspirant_character_by_tm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspirants',
            name='tm_verified',
            field=models.BooleanField(default=False),
        ),
    ]
