# Generated by Django 2.2.7 on 2020-01-09 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20200108_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicidad',
            name='hits',
            field=models.IntegerField(default=0, verbose_name='Hits del Anuncio'),
        ),
    ]
