# Generated by Django 3.1.5 on 2021-05-07 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_auto_20210505_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Field_Office_Id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
