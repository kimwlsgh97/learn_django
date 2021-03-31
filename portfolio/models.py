from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
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
    portname = models.CharField(blank=True, null=True, max_length=200)
    port_price = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.portname

class Sector(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    port = models.ForeignKey('portfolio.Myport', on_delete=models.CASCADE, related_name='sectors')
    sector_name = models.CharField(blank=True, null=True, max_length=200)
    sector_per = models.IntegerField(blank=True, null=True)
    sector_price = models.IntegerField(default=0)

    def __str__(self):
        return self.sector_name

class Mycorp(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    port = models.ForeignKey('portfolio.Myport', on_delete=models.CASCADE, related_name='corps', null=True)
    sector = models.ForeignKey('portfolio.Sector', on_delete=models.CASCADE, related_name='corps', null=True)
    stock_code = models.TextField(blank=True, null=True)
    stock_name = models.TextField(blank=True, null=True)
    stock_count = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    info = models.ForeignKey("portfolio.Corp", on_delete=models.CASCADE, related_name='info', null=True)

    def __str__(self):
        return self.stock_name

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
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock_name