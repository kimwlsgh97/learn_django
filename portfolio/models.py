from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
# class Feedback(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     comment = models.TextField()
#     createDate = models.DateTimeField()

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Corp(models.Model):
    corp_id = models.IntegerField(primary_key=True)
    corp_name = models.CharField(max_length=100, unique=True)
    stock_code = models.IntegerField(null=True)
    stock_price = models.IntegerField(null=True)
    stock_num = models.IntegerField(null=True)