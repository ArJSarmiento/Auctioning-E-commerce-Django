# Generated by Django 3.2.3 on 2021-06-13 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210613_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=0),
        ),
    ]