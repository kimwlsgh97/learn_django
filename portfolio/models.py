from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('portfolio.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

#############################################################
class Myport(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    portname = models.CharField(max_length=200)
    created_date = models.DateTimeField(timezone.now())

class Sector(models.Model):
    port = models.ForeignKey('portfolio.Myport', on_delete=models.CASCADE, related_name='sectors')
    sector_name = models.CharField(max_length=200)
    sector_per = models.IntegerField(blank=True, null=True)

class Mycorp(models.Model):
    sector = models.ForeignKey('portfolio.Sector', on_delete=models.CASCADE, related_name='corps')
    stock_code = models.TextField(unique=True, blank=True, null=True)
    stock_name = models.TextField(unique=True, blank=True, null=True)
    stock_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(timezone.now())

#############################################################


class Corp(models.Model):
    stock_code = models.TextField(blank=True, null=True)
    stock_name = models.TextField(blank=True, null=True)
    stock_price = models.IntegerField(blank=True, null=True)
    high_price = models.IntegerField(blank=True, null=True)
    low_price = models.IntegerField(blank=True, null=True)
    end_price = models.IntegerField(blank=True, null=True)
    sell_count = models.IntegerField(blank=True, null=True)
    sell_price = models.IntegerField(blank=True, null=True)
    updown = models.FloatField(blank=True, null=True)
