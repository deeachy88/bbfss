# Generated by Django 3.1.7 on 2021-07-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_service', '0015_t_inspection_monitoring_t4_collection_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_feebback',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Reference_No', models.CharField(blank=True, max_length=100, null=True)),
                ('Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Address', models.TextField(blank=True, null=True)),
                ('Email', models.CharField(blank=True, max_length=100, null=True)),
                ('Contact_No', models.IntegerField(blank=True, null=True)),
                ('Feedback_Category', models.DateField(blank=True, default=None, null=True)),
                ('Feedback', models.TextField(blank=True, null=True)),
                ('Created_By', models.IntegerField(blank=True, null=True)),
                ('Created_Date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
