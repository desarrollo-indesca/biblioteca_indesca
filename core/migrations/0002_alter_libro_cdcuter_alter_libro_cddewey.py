# Generated by Django 4.2.8 on 2023-12-28 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='cdcuter',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Código de Cuter'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='cddewey',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Código de Dewey'),
        ),
    ]
