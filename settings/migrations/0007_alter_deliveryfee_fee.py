# Generated by Django 4.2.19 on 2025-02-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_deliveryfee_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryfee',
            name='fee',
            field=models.FloatField(blank=True, default=50, null=True),
        ),
    ]
