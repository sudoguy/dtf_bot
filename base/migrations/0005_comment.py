# Generated by Django 2.2.1 on 2019-05-23 20:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_skippedentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('reply_to', models.IntegerField()),
                ('is_favorited', models.BooleanField()),
                ('is_pinned', models.BooleanField()),
                ('is_edited', models.BooleanField()),
                ('level', models.SmallIntegerField()),
                ('source_id', models.SmallIntegerField(choices=[(0, 'Other'), (1, 'Android'), (2, 'iOS')])),
                ('last_response', django.contrib.postgres.fields.jsonb.JSONField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Entry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
