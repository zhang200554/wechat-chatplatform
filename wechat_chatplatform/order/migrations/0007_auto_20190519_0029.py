# Generated by Django 2.1.7 on 2019-05-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20190519_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(default=1, verbose_name='件数'),
        ),
    ]
