# Generated by Django 2.2.6 on 2021-07-26 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(editable=False, max_length=250, verbose_name='confirmation_code'),
        ),
    ]