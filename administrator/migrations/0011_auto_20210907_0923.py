# Generated by Django 3.1.7 on 2021-09-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0010_merge_20210907_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_user_master',
            name='Dzongkhag_Code',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_village_master',
            name='Village_Name_Dzo',
            field=models.CharField(max_length=100),
        ),
    ]