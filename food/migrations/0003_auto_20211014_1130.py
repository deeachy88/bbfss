# Generated by Django 3.1.5 on 2021-10-14 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20210825_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_import_permit_inspection_t2',
            name='Quantity_Balance_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_business_registration_licensing_t5',
            name='Observation',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
