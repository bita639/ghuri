# Generated by Django 3.0.7 on 2020-06-21 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200622_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL),
        ),
    ]