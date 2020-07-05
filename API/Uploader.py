from __future__ import unicode_literals

import json
from datetime import datetime

from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .models import BusinessFile, MessageFile, ServiceFile, Service, Business
from uuid import uuid4
import API.orm as orm

class Image(APIView):


    def put(self, request, format=None, *args, **kwargs):
        try:
            user_id = request.GET['userId']
        except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

        picture = request.FILES['picture']
        if request.data.get('serviceId'):
            service_id = request.data['serviceId']
            orm.insert(ServiceFile,service_id=service_id,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(ServiceFile,service_id=service_id,address=picture.name+"|"+picture.content_type)[0])

            file = open("uploads/service/" + picture.name, 'wb')
            for byte in picture:
                file.write(bytearray(byte))
            file.close()
            return Response({"pic":pic}, status=status.HTTP_200_OK)
        elif request.data.get('businessId'):
            business_id = request.data['businessId']
            orm.insert(BusinessFile,service_id=business_id,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(BusinessFile,business_id=business_id,address=picture.name+"|"+picture.content_type)[0])

            file = open("uploads/business/" + picture.name, 'wb')
            for byte in picture:
                file.write(bytearray(byte))
            file.close()
            return Response({"pic":pic}, status=status.HTTP_200_OK)
        elif request.data.get('messageId'):
            messageId = request.data['messageId']
            orm.insert(MessageFile,messageId=messageId,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(MessageFile,messageId=messageId,address=picture.name+"|"+picture.content_type)[0])
            file = open("uploads/message/"+ picture.name, 'wb')

            for byte in picture:
                file.write(bytearray(byte))
            file.close()
            return Response({"pic":pic}, status=status.HTTP_200_OK)
        return Response({"pic":"کیرم توش"}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request, format=None, *args, **kwargs):
        message = int(request.data.get('message',0))
        id = request.data.get('id',None)
        userId = request.GET.get("userId")

        if id is None:
            return HttpResponse(json.dumps({"error":"id ارسال نشده است"}).encode(),status=400,content_type="application/json")
        if int(request.data.get('serviceId',0)):
            service_id = request.data['serviceId']
            # if len(orm.select(Business,id=orm.select(Service,id=service_id)[0].business_id,owner_id=userId)) ==0:
            #     return HttpResponse(json.dumps({"error": "سرویس متعلق به شما نیست"}).encode(), status=400,
            #                         content_type="application/json")
            pic = orm.select(ServiceFile,service_id=service_id,id=id)
            if len(pic) == 0:
                pic =  orm.select(ServiceFile)[0]
            data = pic[0].address.split("|")
            file = open("uploads/service/" + data[0], 'rb')
            return HttpResponse(file.read(), content_type=data[1])

        elif int(request.data.get('businessId',0)):
            business_id = request.data['businessId']
            # if len(orm.select(Business,id=business_id,user_id=userId)) ==0:
            #     return HttpResponse(json.dumps({"error": "بیزینس متعلق به شما نیست"}).encode(), status=400,
            #                         content_type="application/json")
            pic = orm.select(BusinessFile,service_id=business_id,id=id)
            data = pic[0].address.split("|")
            file = open("uploads/business/" + data[0], 'rb')
            return HttpResponse(file.read(), content_type=data[1])

        elif int(request.data.get('messageId',0)):
            messageId = request.data['messageId']
            pic = orm.select(MessageFile,messageId=messageId,id=id)
            data = pic[0].address.split("|")
            file = open("uploads/message/" + data[0])
            return HttpResponse(file.read(), content_type=data[1])


