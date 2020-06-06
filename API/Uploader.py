from __future__ import unicode_literals

from datetime import datetime

from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from  .models import BusinessFile,MessageFile,ServiceFile
from uuid import uuid4
import API.orm as orm

class Image(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None, *args, **kwargs):
        # user_id = request.GET['userId']
        service = int(request.POST.get('service',0))
        business = int(request.POST.get('business',0))
        message = int(request.POST.get('message',0))
        picture = request.FILES['picture']
        address = uuid4().__str__()
        if service:
            service_id = request.POST['serviceId']
            orm.insert(ServiceFile,service_id=service_id,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(BusinessFile,messageId=ServiceFile,address=picture.name+"|"+picture.content_type)[0])

            file = open("uploads/service/" + picture.name, 'wb')

        elif business:
            business_id = request.POST['businessId']
            orm.insert(BusinessFile,service_id=business_id,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(BusinessFile,messageId=messageId,address=picture.name+"|"+picture.content_type)[0])

            file = open("uploads/business/" + picture.name, 'wb')

        elif message:
            messageId = request.POST['messageId']
            orm.insert(MessageFile,messageId=messageId,address=picture.name+"|"+picture.content_type)
            pic = orm.toDict(orm.select(MessageFile,messageId=messageId,address=picture.name+"|"+picture.content_type)[0])
            file = open("uploads/message/"+ picture.name, 'wb')

        for byte in picture:
            file.write(bytearray(byte))
        file.close()
        return Response({"pic":pic}, status=status.HTTP_200_OK)


    def post(self, request, format=None, *args, **kwargs):
        service = int(request.POST.get('service',0))
        business = int(request.POST.get('business',0))
        message = int(request.POST.get('message',0))
        id = request.POST.get('id',1)

        if service:
            service_id = request.POST['serviceId']
            pic = orm.select(ServiceFile,service_id=service_id,id=id)
            data = pic[0].address.split("|")
            file = open("uploads/service/" + data[0], 'rb')
            return HttpResponse(file.read(), content_type=data[1])

        elif business:
            business_id = request.POST['businessId']
            pic = orm.select(BusinessFile,service_id=business_id,id=id)
            data = pic[0].address.split("|")
            file = open("uploads/business/" + data[0], 'rb')
            return HttpResponse(file.read(), content_type=data[1])

        elif message:
            messageId = request.POST['messageId']
            pic = orm.select(MessageFile,messageId=messageId,id=id)
            data = pic[0].address.split("|")
            file = open("uploads/message/" + data[0])
            return HttpResponse(file.read(), content_type=data[1])


