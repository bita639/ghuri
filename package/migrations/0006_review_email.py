# Generated by Django 3.0.7 on 2020-10-19 23:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0005_auto_20201020_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]