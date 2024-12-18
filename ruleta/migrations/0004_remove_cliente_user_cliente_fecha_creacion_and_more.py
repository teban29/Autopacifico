# Generated by Django 5.1.3 on 2024-12-03 05:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleta', '0003_alter_cliente_numero_factura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='user',
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_factura',
            field=models.CharField(max_length=50),
        ),
    ]
