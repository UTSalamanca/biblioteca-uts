# Generated by Django 5.0.6 on 2024-08-06 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0015_alter_acervo_model_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acervo_model',
            old_name='fecha_edicion',
            new_name='fechaedicion',
        ),
        migrations.RenameField(
            model_name='acervo_model',
            old_name='fecha_registro',
            new_name='fecharegistro',
        ),
    ]