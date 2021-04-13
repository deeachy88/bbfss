# Generated by Django 3.1.5 on 2021-04-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0006_auto_20210406_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_plant_import_permit_t1',
            name='Country_Of_Origin',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_plant_movement_permit_t1',
            name='Qty',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='t_plant_movement_permit_t1',
            name='Unit',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]