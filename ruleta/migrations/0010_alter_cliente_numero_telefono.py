# Generated by Django 5.1.3 on 2024-12-03 17:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleta', '0009_cliente_fecha_creacion_cliente_numero_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='numero_telefono',
            field=models.CharField(default=0, max_length=15, validators=[django.core.validators.RegexValidator(message="El número de teléfono debe contener entre 7 y 15 dígitos, y puede incluir un '+' inicial.", regex='^\\+?[0-9]{7,15}$')]),
            preserve_default=False,
        ),
    ]
