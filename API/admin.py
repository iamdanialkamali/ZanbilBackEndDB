from django.contrib import admin
from .models import  Business, Category, Service, TimeTable, Reserve, Sans, Transaction, Wallet, Review, \
    BusinessFile, ServiceFile, MessageFile

admin.site.register(Business)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(TimeTable)
admin.site.register(Reserve)
admin.site.register(Sans)
admin.site.register(Wallet)
admin.site.register(Review)
admin.site.register(Transaction)
admin.site.register(BusinessFile)
admin.site.register(ServiceFile)
admin.site.register(MessageFile)

# Register your models here.
