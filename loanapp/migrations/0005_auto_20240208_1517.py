# Generated by Django 3.0 on 2024-02-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanapp', '0004_auto_20240208_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
