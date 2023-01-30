# Generated by Django 4.0.4 on 2022-08-29 07:21

import base.helpers
import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_category_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(default=base.helpers.uuid, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=1055)),
                ('answer', models.CharField(max_length=1055)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question',
                'ordering': ['-created_at'],
            },
            bases=(base.models.BaseModel, models.Model),
        ),
    ]
