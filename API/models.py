# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime,time

from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    credit = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='businesses')
    name = models.CharField(max_length=100)
    phone_number = models.TextField(max_length=15)
    score = models.FloatField(default=0)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=600, default='test')

    def __str__(self):
        return str(self.name)




class TimeTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,default="timeTable")
    business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, related_name='timeTables')

    def __str__(self):
        return str(self.name)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, related_name='services')
    timeTable = models.ForeignKey(TimeTable, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=500)
    fee = models.FloatField()
    rating = models.FloatField(default=0)
    reviewCount = models.IntegerField(default=0)
    description = models.TextField(max_length=600, blank=True)
    cancellation_range = models.IntegerField(default=None,null=True)
    wallet = models.ForeignKey(to=Wallet,null=True, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name


class Sans(models.Model):
    id = models.AutoField(primary_key=True)
    startTime = models.TimeField(default=time(0,0,0))
    endTime = models.TimeField(default=time(0,0,0))
    timeTable = models.ForeignKey(to=TimeTable, on_delete=models.DO_NOTHING, related_name='sanses')
    weekDay = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.startTime) + "-->" + str(self.endTime)


class Reserve(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(to=Service, on_delete=models.DO_NOTHING, null=True)
    sans = models.ForeignKey(Sans, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)
    isCancelled = models.BooleanField(default=False)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=600, default='')
    rating = models.FloatField()
    reserve = models.ForeignKey(Reserve, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.description


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    reserve = models.ForeignKey(Reserve, on_delete=models.DO_NOTHING, null=True, blank=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    paidAt = models.DateTimeField()
    amount = models.FloatField()

    def __str__(self):
        return self.paidAt.__str__() + " " + self.amount.__str__()


class BusinessFile(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(null=True, max_length=200)
    business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, null=True, related_name='pictures')


class ServiceFile(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(null=True, max_length=200)
    service = models.ForeignKey(to=Service, on_delete=models.DO_NOTHING, null=True, related_name='pictures')


class MessageFile(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(null=True, max_length=200)
    ticketId = models.TextField(null=True)


class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.TextField(null=True)
    url = models.TextField(null=True)
    request = models.TextField(null=True)
    response = models.TextField(null=True)
    createdAt = models.DateTimeField(null=True)
