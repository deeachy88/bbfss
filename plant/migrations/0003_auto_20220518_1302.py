# Generated by Django 3.1.5 on 2022-05-18 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0002_auto_20220429_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_payment_details_master',
            old_name='account_head_code',
            new_name='accountHeadId',
        ),
        migrations.RenameField(
            model_name='t_payment_details_master',
            old_name='service_fee',
            new_name='serviceFee',
        ),
        migrations.AlterField(
            model_name='t_payment_details_master',
            name='account_head_name',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]