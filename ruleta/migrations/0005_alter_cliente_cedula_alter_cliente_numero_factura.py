# Generated by Django 5.1.3 on 2024-12-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleta', '0004_remove_cliente_user_cliente_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_factura',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]