# Generated by Django 3.1.5 on 2021-04-28 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20210428_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_food_licensinf_food_handler_t1',
            old_name='Training_Date',
            new_name='Training_From_Date',
        ),
        migrations.AddField(
            model_name='t_food_licensinf_food_handler_t1',
            name='Training_To_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]