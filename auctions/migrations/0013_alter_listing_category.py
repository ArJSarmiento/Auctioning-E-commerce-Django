# Generated by Django 3.2.3 on 2021-06-16 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('NG', 'No Category'), ('MA', 'Mens Apparel'), ('WA', 'Womens Apparel'), ('SP', 'Sports'), ('HM', 'Home'), ('TY', 'Toys')], default='NG', max_length=2),
        ),
    ]
