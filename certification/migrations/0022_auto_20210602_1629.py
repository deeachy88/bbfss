# Generated by Django 3.1.5 on 2021-06-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0021_auto_20210601_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_certification_food_t1',
            name='Audit_Plan_Acceptance',
            field=models.CharField(blank=True, default='R', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_gap_t1',
            name='Audit_Plan_Acceptance',
            field=models.CharField(blank=True, default='R', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_organic_t1',
            name='Audit_Plan_Acceptance',
            field=models.CharField(blank=True, default='R', max_length=10, null=True),
        ),
    ]
