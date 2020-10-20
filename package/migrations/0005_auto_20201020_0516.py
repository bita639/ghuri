# Generated by Django 3.0.7 on 2020-10-19 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('package', '0004_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('created',)},
        ),
        migrations.RenameField(
            model_name='review',
            old_name='review_desc',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='commented_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='review',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_id',
        ),
        migrations.AddField(
            model_name='review',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='review',
            name='comment_user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_user_id', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='package_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='package.Package'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]