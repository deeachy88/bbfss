# Generated by Django 3.1.7 on 2021-06-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_service', '0009_t_commodity_inspection_t1_t_commodity_inspection_t2'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_commodity_inspection_t1',
            name='Created_By',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_commodity_inspection_t1',
            name='Created_On',
            field=models.DateField(blank=True, null=True),
        ),
    ]
