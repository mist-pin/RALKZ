# Generated by Django 4.2.11 on 2024-04-20 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0008_alter_employee_join_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='join_date',
            field=models.DateField(auto_now=True),
        ),
    ]
