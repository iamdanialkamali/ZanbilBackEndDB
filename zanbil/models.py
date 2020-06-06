# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# from django.contrib.auth.models import User
# from django.db import models
#
#
# class Category(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=300)
#
#     def __str__(self):
#         return self.name
#
#
# class Business(models.Model):
#     id = models.AutoField(primary_key=True)
#     owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
#     category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='businesses')
#     name = models.CharField(max_length=100)
#     phone_number = models.TextField(max_length=15)
#     score = models.FloatField(default=0)
#     address = models.TextField(max_length=500)
#     description = models.TextField(max_length=600, default='test')
#
#     def __str__(self):
#         return str(self.name)
#
#     def calculateScore(self, sc):
#         return (self.score + sc) / 2
#
#
# class TimeTable(models.Model):
#     id = models.AutoField(primary_key=True)
#     business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, related_name='timetables')
#
#
# class Service(models.Model):
#     id = models.AutoField(primary_key=True)
#     business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, related_name='services')
#     timetable = models.ForeignKey(TimeTable, on_delete=models.DO_NOTHING)
#     name = models.CharField(max_length=30)
#     address = models.TextField(max_length=500)
#     fee = models.FloatField()
#     rating = models.FloatField(default=0)
#     description = models.TextField(max_length=600, blank=True)
#     # review_count = models.IntegerField(default=0)
#     # is_protected = models.BooleanField(default=False)
#     # password = models.CharField(max_length=500)
#     cancellation_range = models.CharField(default="00:00", max_length=5)
#
#     def __str__(self):
#         return self.name
#
#
#
# class Sans(models.Model):
#     id = models.AutoField(primary_key=True)
#     startTime = models.CharField(default="00:00", max_length=5)
#     endTime = models.CharField(default="00:00", max_length=5)
#     timeTable = models.ForeignKey(to=TimeTable, on_delete=models.DO_NOTHING, related_name='sanses')
#     weekDay = models.PositiveSmallIntegerField(default=0)
#
#     def __str__(self):
#         return str(self.start_time) + ' : ' + str(self.end_time)
#
#
# class Reserve(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     service = models.ForeignKey(to=Service, on_delete=models.DO_NOTHING, null=True)
#     sans = models.ForeignKey(Sans, on_delete=models.DO_NOTHING, null=True, blank=True)
#     description = models.TextField()
#     date = models.CharField(max_length=150)
#     isCancelled = models.BooleanField(default=False)
#
#
# class Review(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.CharField(max_length=600, default='')
#     rating = models.FloatField()
#     reserve = models.ForeignKey(Reserve, on_delete=models.DO_NOTHING, null=True, blank=True)
#
#     def __str__(self):
#         return self.description
#
#
# class Transaction(models.Model):
#     id = models.AutoField(primary_key=True)
#     reserve = models.ForeignKey(Reserve, on_delete=models.DO_NOTHING, null=True, blank=True)
#     paidAt = models.DateTimeField()
#     amount = models.FloatField()
#
#     def __str__(self):
#         return self.paidAt.__str__() + " " + self.amount
#
#
#
# class File(models.Model):
#     id = models.AutoField(primary_key=True)
#     address = models.CharField(null=True, max_length=200)
#     business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, null=True, related_name='pictures')
#     service = models.ForeignKey(to=Service, on_delete=models.DO_NOTHING, null=True, related_name='pictures')
#     message = models.TextField(null=True)
#
