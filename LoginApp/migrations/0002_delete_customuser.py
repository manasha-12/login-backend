# Generated by Django 5.0.3 on 2024-03-11 11:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("LoginApp", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
