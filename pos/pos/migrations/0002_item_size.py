# Generated by Django 4.2.1 on 2023-05-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]