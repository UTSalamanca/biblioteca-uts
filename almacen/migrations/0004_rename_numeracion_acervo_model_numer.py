# Generated by Django 5.0.4 on 2024-05-16 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0003_acervo_model_numeracion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acervo_model',
            old_name='numeracion',
            new_name='numer',
        ),
    ]
