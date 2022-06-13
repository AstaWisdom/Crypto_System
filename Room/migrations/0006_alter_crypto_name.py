# Generated by Django 4.0.1 on 2022-02-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0005_remove_crypto_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='name',
            field=models.CharField(choices=[('BTC-USDT', 'BTC-USDT'), ('ETH-USDT', 'ETH-USDT')], max_length=50),
        ),
    ]