# Generated by Django 5.0.6 on 2024-08-14 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadias', '0012_alter_model_estadias_matricula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_estadias',
            name='carrera',
            field=models.CharField(max_length=20),
        ),
    ]
