# Generated by Django 3.1.5 on 2021-04-21 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0014_auto_20210421_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_livestock_export_certificate_t2',
            name='Unit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
