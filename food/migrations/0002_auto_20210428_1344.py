# Generated by Django 3.1.5 on 2021-04-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_food_licensinf_food_handler_t1',
            name='Application_No',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]