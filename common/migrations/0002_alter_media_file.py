# Generated by Django 5.0.3 on 2024-03-07 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
