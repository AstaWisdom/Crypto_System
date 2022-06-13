# Generated by Django 4.0.1 on 2022-02-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0003_userinfo_money_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='chart',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='crypto',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='crypto',
            name='indicator_chart_ma',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='crypto',
            name='indicator_chart_macd',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='crypto',
            name='indicator_chart_rsi',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='crypto',
            name='indicator_chart_stockhastic',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
