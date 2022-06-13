from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class App(models.Model):
    version = models.CharField(max_length=256, null=False, blank=False)
    application = models.FileField(upload_to='media')

    def __str__(self):
        return self.application


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50, null=False)
    family_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    money_amount = models.IntegerField(default=0)
    cliend_oid = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"user: {self.user} , name: {self.name}"



class Crypto(models.Model):
    c = [('BTC-USD', 'BTC-USD'), ('ETH-USD', 'ETH-USD')]
    crypto_type = models.CharField(max_length=50, choices=c, null=True)
    name = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField(null=True)
    order_amount = models.IntegerField(null=True)
    type_choice = [('Buy', 'Buy'), ('Sell', 'Sell')]
    order_type = models.CharField(choices=type_choice, max_length=50, null=True)
    order_size = models.IntegerField(null=True)
    complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        ord_id = self.order_id
        has_ord_id = Orders.objects.filter(order_id=ord_id).exists()
        count = 1

        while has_ord_id:
            ord_id += count
            has_ord_id = Orders.objects.filter(order_id=ord_id).exists()
        self.order_id = ord_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


