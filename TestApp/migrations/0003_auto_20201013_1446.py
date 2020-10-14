# Generated by Django 3.0.7 on 2020-10-13 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TestApp', '0002_auto_20201013_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner1_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_id', to='TestApp.Recipe'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='I_recipe', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
