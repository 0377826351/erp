# Generated by Django 4.0.4 on 2022-08-01 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_article_created_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
