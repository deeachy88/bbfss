# Generated by Django 3.1.5 on 2021-05-12 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Certificate_Type',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Certificate_Type',
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Farm_Location',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_organic_t1',
            name='Farm_Location',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]