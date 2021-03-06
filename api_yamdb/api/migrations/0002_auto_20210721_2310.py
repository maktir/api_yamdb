# Generated by Django 2.2.6 on 2021-07-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=200, unique=True, verbose_name='Название категории'), null=True, unique=True),
        ),
    ]
