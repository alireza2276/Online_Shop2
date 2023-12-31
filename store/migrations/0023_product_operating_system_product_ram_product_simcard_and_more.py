# Generated by Django 4.2.7 on 2023-12-17 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_product_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='operating_system',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='ram',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='simcard',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(max_length=255, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='body',
            field=models.TextField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='full_name'),
        ),
    ]
