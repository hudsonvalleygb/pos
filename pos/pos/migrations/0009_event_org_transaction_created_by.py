# Generated by Django 4.2.1 on 2023-05-16 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pos', '0008_organization_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos.organization'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]