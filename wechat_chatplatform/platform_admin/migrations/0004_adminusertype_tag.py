# Generated by Django 2.1.7 on 2019-05-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_admin', '0003_auto_20190517_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminusertype',
            name='tag',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='标签'),
        ),
    ]
