# Generated by Django 4.1.4 on 2023-01-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='organization',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='staff',
            field=models.BooleanField(default=True),
        ),
    ]
