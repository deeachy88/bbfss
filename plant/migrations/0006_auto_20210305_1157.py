# Generated by Django 3.1.5 on 2021-03-05 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0005_auto_20210305_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_file_attachment',
            name='Attachment',
            field=models.FileField(upload_to='plant'),
        ),
    ]
