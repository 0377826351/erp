# Generated by Django 4.0.4 on 2022-08-03 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
    ]
