# Generated by Django 3.0.7 on 2020-10-12 18:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0004_auto_20201013_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourtype',
            name='package_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='T_package_id', to='package.Package'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TourTypePackage',
        ),
    ]