# Generated by Django 3.1.7 on 2021-03-31 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0002_auto_20210331_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_livestock_clearence_meat_shop_t1',
            name='Conformity',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
