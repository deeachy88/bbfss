# Generated by Django 3.1.5 on 2022-06-23 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Validity_Period',
        ),
        migrations.AddField(
            model_name='t_certification_organic_t1',
            name='Issue_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
