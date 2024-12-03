# Generated by Django 5.1.3 on 2024-12-03 06:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleta', '0007_cliente_user_alter_cliente_cedula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='telefono',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_factura',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9-]+$', 'El número de factura debe contener solo letras, números y guiones.')]),
        ),
        migrations.AddIndex(
            model_name='ganador',
            index=models.Index(fields=['fecha'], name='ruleta_gana_fecha_6f71da_idx'),
        ),
    ]
