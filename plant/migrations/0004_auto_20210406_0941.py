# Generated by Django 3.1.5 on 2021-04-06 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0003_auto_20210406_0925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_plant_clearence_nursery_seed_grower_t2',
            old_name='Variety_Id',
            new_name='Variety',
        ),
        migrations.RemoveField(
            model_name='t_plant_clearence_nursery_seed_grower_t2',
            name='Crop_Category_Id',
        ),
        migrations.RemoveField(
            model_name='t_plant_clearence_nursery_seed_grower_t2',
            name='Crop_Id',
        ),
        migrations.AddField(
            model_name='t_plant_clearence_nursery_seed_grower_t2',
            name='Crop',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='t_plant_clearence_nursery_seed_grower_t2',
            name='Crop_Category',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]