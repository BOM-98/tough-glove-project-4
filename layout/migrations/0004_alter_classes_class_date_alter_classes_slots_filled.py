# Generated by Django 4.1 on 2023-10-16 20:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("layout", "0003_alter_members_options_remove_members_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classes",
            name="class_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="classes",
            name="slots_filled",
            field=models.IntegerField(default=0),
        ),
    ]