# Generated by Django 3.1.5 on 2021-04-06 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0002_auto_20210406_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_plant_clearence_nursery_seed_grower_t1',
            name='CID',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='t_plant_clearence_nursery_seed_grower_t1',
            name='contactNo',
            field=models.BigIntegerField(),
        ),
    ]