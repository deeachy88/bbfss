# Generated by Django 3.1.5 on 2021-05-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0010_auto_20210517_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_certification_food_t1',
            name='Others_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_food_t1',
            name='Terms_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Others_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Terms_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_organic_t1',
            name='Others_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_organic_t1',
            name='Terms_Standards',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
