# Generated by Django 4.0.4 on 2022-08-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
