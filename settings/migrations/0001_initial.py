# Generated by Django 4.2.19 on 2025-02-15 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='company_logos')),
                ('subtitle', models.TextField(blank=True, max_length=1000, null=True)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('instgram_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phones', models.CharField(blank=True, max_length=255, null=True)),
                ('android_app', models.URLField(blank=True, null=True)),
                ('ios_app', models.URLField(blank=True, null=True)),
                ('call_us', models.CharField(blank=True, max_length=255, null=True)),
                ('email_us', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.FloatField()),
            ],
        ),
    ]
