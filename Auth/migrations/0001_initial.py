# Generated by Django 4.2.10 on 2024-03-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RalkzUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField(max_length=200)),
                ('email', models.EmailField(max_length=30, null=True, unique=True)),
                ('full_name', models.CharField(default='NULL', max_length=30)),
                ('accept_privacy_policy', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_aspirant', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
                ('pass_hist', models.TextField(max_length=10000)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
