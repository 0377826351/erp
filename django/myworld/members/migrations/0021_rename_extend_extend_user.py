# Generated by Django 4.0.4 on 2022-08-10 09:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0020_extend'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Extend',
            new_name='Extend_User',
        ),
    ]
