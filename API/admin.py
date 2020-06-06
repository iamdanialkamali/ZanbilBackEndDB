from django.contrib import admin
from .models import User,Business,Category,Service,TimeTable,Reserve,Sans,Transaction

admin.site.register(Business)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(TimeTable)
admin.site.register(Reserve)
admin.site.register(Sans)
admin.site.register(Transaction)

# Register your models here.
