# Generated by Django 3.1.5 on 2021-05-25 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_t_inspection_type_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_food_category_master',
            fields=[
                ('Category_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Category_Name', models.CharField(max_length=100)),
                ('HS_Code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_category_master',
            fields=[
                ('Category_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Category_Name', models.CharField(default=None, max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_product_master',
            fields=[
                ('Product_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Product_Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_species_master',
            fields=[
                ('Species_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Species_Name', models.CharField(max_length=150)),
                ('Category_Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.t_livestock_category_master')),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_species_breed_master',
            fields=[
                ('Species_Breed_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Species_Breed_Name', models.CharField(max_length=150)),
                ('Category_Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.t_livestock_category_master')),
                ('Species_Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.t_livestock_species_master')),
            ],
        ),
    ]
