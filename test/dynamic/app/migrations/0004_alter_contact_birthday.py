# Generated by Django 4.0.4 on 2022-08-26 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
