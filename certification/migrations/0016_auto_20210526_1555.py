# Generated by Django 3.1.5 on 2021-05-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0015_auto_20210526_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_certification_gap_t8',
            name='Non_Conformity_Category',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_gap_t8',
            name='Non_Conformity_Description',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
