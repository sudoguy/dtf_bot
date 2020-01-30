# Generated by Django 2.2.9 on 2020-01-30 14:09

from django.db import migrations


def forwards(apps, schema_editor):
    SkippedEntry = apps.get_model('base', 'SkippedEntry')
    Skipped = apps.get_model('base', 'Skipped')

    Skipped.objects.bulk_create(
        Skipped(object_type="entry", object_id=entry.id)
        for entry in SkippedEntry.objects.all()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20200130_1408'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
