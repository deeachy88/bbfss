# Generated by Django 3.1.5 on 2021-08-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_certification_gap_t8',
            name='Corrective_Action_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t8',
            name='Corrective_Action_Taken_Auditee',
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Corrective_Action_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Corrective_Action_Taken_Auditee',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_gap_t1',
            name='Audit_Team_Acceptance',
            field=models.CharField(blank=True, default='R', max_length=1, null=True),
        ),
    ]
