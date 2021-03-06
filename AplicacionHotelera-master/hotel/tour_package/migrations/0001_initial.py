# Generated by Django 2.2.4 on 2020-01-07 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accesos', '0001_initial'),
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Titulo del Paquete')),
                ('description', models.CharField(max_length=250, verbose_name='Descripcion del Paquete')),
                ('available_stock', models.IntegerField(default=30, verbose_name='Stock')),
                ('company', models.CharField(max_length=120, verbose_name='Compania')),
                ('days', models.CharField(max_length=150, verbose_name='Dia')),
                ('hours', models.CharField(max_length=100, verbose_name='Hora')),
                ('price', models.IntegerField(default=0, verbose_name='Precio')),
                ('path_image', models.FileField(blank=True, max_length=250, null=True, upload_to='', verbose_name='Url de Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='TourOrder',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shopping_cart.Product')),
                ('reservation_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesos.Perfil')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tour_package.Tour_Package')),
            ],
            bases=('shopping_cart.product',),
        ),
    ]
