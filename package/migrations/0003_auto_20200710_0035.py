# Generated by Django 3.0.7 on 2020-07-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_auto_20200710_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='special_offer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]