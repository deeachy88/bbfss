# Generated by Django 3.1.5 on 2021-05-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0018_auto_20210516_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='FI_Inspection_Team',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='FR_Inspection_Team',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
