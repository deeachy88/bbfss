# Generated by Django 3.1.5 on 2021-05-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_t_food_business_registration_licensing_t6'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t5',
            name='Clause_No',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t5',
            name='Concern',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t5',
            name='Date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]