#  MODELS  ( DATABASE  STRUCTURES )  DEFINED  HERE
from django.db import models

class weathersensors(models.Model):
    temp = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    altitude = models.FloatField()
    seapressure = models.FloatField()
    userid = models.IntegerField()
    plant_id = models.IntegerField()
    time = models.TimeField(null=True)
    date = models.DateField(null=True)
    rain = models.IntegerField(null = True, default = 0)

    def __str__(self):
        return str(self.date) + ' - ' + str(self.time) + '(' + str(self.id) + ')'

class plantsensors(models.Model):
    entryid = models.ForeignKey(weathersensors, on_delete = models.CASCADE)
    soilmoisture = models.FloatField()
    def __str__(self):
        return str(self.entryid)


class reservoir(models.Model):
    entryid = models.ForeignKey(weathersensors, on_delete = models.CASCADE)
    distance = models.FloatField()
    actualHieght = models.FloatField(default= 35)
    def __str__(self):
        return str(self.entryid)
