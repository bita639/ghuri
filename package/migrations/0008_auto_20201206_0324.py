# Generated by Django 3.1.1 on 2020-12-05 21:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0007_payagency'),
    ]

    operations = [
        migrations.AddField(
            model_name='customize_tour',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Payment on process', 'Payment on process')], default='Pending', max_length=30, null=True),
        ),
    ]