# Generated by Django 3.2.3 on 2021-06-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210612_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
