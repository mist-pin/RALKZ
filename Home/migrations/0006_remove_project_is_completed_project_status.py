# Generated by Django 4.2.10 on 2024-04-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_alter_project_project_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default='being reviewed', max_length=20),
            preserve_default=False,
        ),
    ]
