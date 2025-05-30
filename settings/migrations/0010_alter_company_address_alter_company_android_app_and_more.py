# Generated by Django 4.2.19 on 2025-02-19 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0009_alter_deliveryfee_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='company',
            name='android_app',
            field=models.URLField(blank=True, null=True, verbose_name='android app'),
        ),
        migrations.AlterField(
            model_name='company',
            name='android_ios_app',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='android ios app'),
        ),
        migrations.AlterField(
            model_name='company',
            name='call_us',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='call us'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email_us',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='email us'),
        ),
        migrations.AlterField(
            model_name='company',
            name='facebook_link',
            field=models.URLField(blank=True, null=True, verbose_name='facebook'),
        ),
        migrations.AlterField(
            model_name='company',
            name='free_home_delivery',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='free home delivery'),
        ),
        migrations.AlterField(
            model_name='company',
            name='instant_return_policy',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='instant return policy'),
        ),
        migrations.AlterField(
            model_name='company',
            name='instgram_link',
            field=models.URLField(blank=True, null=True, verbose_name='instgram'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ios_app',
            field=models.URLField(blank=True, null=True, verbose_name='ios app'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='company_logos', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phones',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='phones'),
        ),
        migrations.AlterField(
            model_name='company',
            name='secure_payment_way',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='secure payment way'),
        ),
        migrations.AlterField(
            model_name='company',
            name='subtitle',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='subtitle'),
        ),
        migrations.AlterField(
            model_name='company',
            name='support_system',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='support system'),
        ),
        migrations.AlterField(
            model_name='company',
            name='twitter_link',
            field=models.URLField(blank=True, null=True, verbose_name='twitter'),
        ),
        migrations.AlterField(
            model_name='deliveryfee',
            name='fee',
            field=models.FloatField(verbose_name='fee'),
        ),
        migrations.AlterField(
            model_name='freeoffer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='freeoffer',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='freeoffer',
            name='image',
            field=models.ImageField(upload_to='product_fee', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='freeoffer',
            name='title',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='title'),
        ),
    ]
