# Generated by Django 4.2.2 on 2023-09-23 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterField(
            model_name="expense",
            name="amount",
            field=models.FloatField(),
        ),
    ]
