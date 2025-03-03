from django.db import models
import datetime
from random import randint

# Create your models here.
class Info(models.Model):
    time = models.DateTimeField()
    temperature = models.FloatField(default=21)
    humidity = models.FloatField(default=50)
    target_temperature = models.FloatField(default=10)
    power = models.BooleanField(default=True)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time} - {self.temperature} - {self.humidity} - {self.target_temperature}"
    
    def update(self):
        self.time = datetime.datetime.now()
        self.save()

class Timer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=False)
    target_temperature = models.FloatField(default=21)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} - {self.length} - {self.active} - {self.target_temperature}"
    
    @property
    def formatted_start_time(self):
        return self.start_time.strftime("%a %d %b %H:%M")
    
    @property
    def formatted_end_time(self):
        return self.end_time.strftime("%a %d %b %H:%M")

