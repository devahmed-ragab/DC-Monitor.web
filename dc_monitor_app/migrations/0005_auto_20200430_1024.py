# Generated by Django 3.0.5 on 2020-04-30 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dc_monitor_app', '0004_auto_20200430_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]