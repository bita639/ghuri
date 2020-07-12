# Generated by Django 3.0.7 on 2020-06-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='languages',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='nationality',
            field=models.CharField(blank=True, choices=[('Bangladeshi', 'Bangladeshi'), ('Indian', 'Indian'), ('Chinese', 'Chinese'), ('Japanese', 'Japanese')], max_length=50, null=True),
        ),
    ]
