# Generated by Django 4.0.4 on 2022-08-29 03:52

import app.modules.category.model
import base.helpers
import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_contact_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(default=base.helpers.uuid, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('id_int', models.IntegerField(default=app.modules.category.model.auto_integer)),
                ('multi_index', models.CharField(max_length=255)),
                ('level', models.IntegerField(default=0)),
                ('total_item', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_created_by', to=settings.AUTH_USER_MODEL)),
                ('parent_id', models.ForeignKey(db_column='parent_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_parent_id', to='app.category')),
                ('update_by', models.ForeignKey(db_column='update_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'category',
                'ordering': ['-id_int'],
            },
            bases=(base.models.BaseModel, models.Model),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.CharField(default=base.helpers.uuid, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=50)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.CharField(max_length=255, null=True)),
                ('video', models.CharField(max_length=255, null=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('content', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category_id', models.ForeignKey(db_column='category_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.category')),
                ('created_by', models.ForeignKey(db_column='created_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_created_by', to=settings.AUTH_USER_MODEL)),
                ('topic_id', models.ForeignKey(db_column='topic_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.document')),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article',
                'ordering': ['created_at'],
            },
            bases=(base.models.BaseModel, models.Model),
        ),
    ]
