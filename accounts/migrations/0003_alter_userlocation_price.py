# Generated by Django 5.0.3 on 2024-04-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
