# Generated by Django 5.0.4 on 2024-11-23 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadias', '0019_alter_model_estadias_carrera_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_view',
            name='id_reporte',
            field=models.IntegerField(null=True),
        ),
    ]
