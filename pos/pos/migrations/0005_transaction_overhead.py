# Generated by Django 4.2.1 on 2023-05-09 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_rename_date_event_start_date_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='overhead',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
