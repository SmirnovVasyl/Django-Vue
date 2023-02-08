from django.db import models

class btc_price(models.Model):
  Date = models.DateTimeField()
  Open = models.FloatField()
  Close = models.FloatField()
  High = models.FloatField()
  Low = models.FloatField()
  Volume = models.FloatField()
