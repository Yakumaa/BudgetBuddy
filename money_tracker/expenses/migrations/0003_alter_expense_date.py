# Generated by Django 4.2.2 on 2023-09-23 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0002_alter_category_options_alter_expense_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
