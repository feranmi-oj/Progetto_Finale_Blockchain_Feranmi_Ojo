from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from .utils import sendTransaction
import hashlib



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usd_balance = models.FloatField(default=0)
    ip_address = models.CharField(max_length=150, blank=True, null=True)
    last_login = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return "{}".format(self.user.username)


class Shoes(models.Model):
    name = models.CharField(max_length=35)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    starting_price = models.FloatField(default=0)
    buy_now = models.FloatField(default=0)
    end_auction = models.DateTimeField(auto_now_add=False ,default=datetime.today())
    offer = models.FloatField(default=0)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=5 ,default='open')
    # Ropsten
    hash = models.CharField(max_length=32, default=None, blank=True,null=True)
    txId = models.CharField(max_length=66,default=None,blank=True, null=True)

    def get_absolute_url(self):
        return reverse('app:show_section', kwargs={'pk': self.pk})

    def get_url(self):
        return reverse('app:make_an_offer', kwargs={'pk': self.pk})
    def write_on_chain(self,jsonData):
        self.hash = hashlib.sha256(jsonData.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

