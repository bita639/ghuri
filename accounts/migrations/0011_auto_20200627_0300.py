# Generated by Django 3.0.7 on 2020-06-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200627_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='photo',
            field=models.FileField(blank=True, default='profileImage/blank.png', null=True, upload_to='profileImage'),
        ),
        migrations.AlterField(
            model_name='agency',
            name='photo',
            field=models.FileField(blank=True, default='profileImage/blank.png', null=True, upload_to='profileImage'),
        ),
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.FileField(blank=True, default='profileImage/blank.png', null=True, upload_to='profileImage'),
        ),
    ]