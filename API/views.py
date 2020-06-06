# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser



from .models import Review,Service
import json
from .Token import Tokenizer as tokenizer
class TEST(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None, *args, **kwargs):
        user_id = request.GET['userId']
        ali = request.FILES['pic']
        print(ali.name)
        file = open("uploads/"+ali.name,'wb')
        for i in ali:
            file.write(bytearray(i))
        file.close()
        return Response({}, status=status.HTTP_200_OK)
