# Generated by Django 4.2.2 on 2023-07-01 15:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0018_result_status_result_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="used",
        ),
    ]