# Generated by Django 3.1.5 on 2021-04-14 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_livestock_export_certificate_t1',
            old_name='Export_Type',
            new_name='Exporter_Type',
        ),
    ]
