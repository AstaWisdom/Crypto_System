# Generated by Django 4.0.1 on 2022-02-25 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0012_orders_userinfo_cliend_oid_delete_payments'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=256)),
                ('application', models.FileField(upload_to='media')),
            ],
        ),
    ]
