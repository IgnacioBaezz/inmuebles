# Generated by Django 5.1.2 on 2024-11-11 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyprice',
            name='status',
            field=models.CharField(choices=[('sell', 'venta'), ('lease', 'arriendo')], default='lease', max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='message',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Mensaje'),
        ),
    ]
