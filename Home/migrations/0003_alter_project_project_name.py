# Generated by Django 4.2.10 on 2024-03-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_remove_employeeposition_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
