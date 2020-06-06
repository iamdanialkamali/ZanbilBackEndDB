import json
from django.core import serializers as djserializers
from django.http import HttpResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from zanbil.models import User
from zanbil.serializer import *
from zanbil.serializer import *
from zanbil.models import *
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import mixins

from zanbil.validation import DataValidator


class UserAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


    def put(self, request, format=None):
        data = request.POST
        # users = User.objects.raw("INSERT INTO auth_user ")
        validator = DataValidator(data)
        validator. \
            fieldValidator. \
            checkNotNone("username"). \
            checkNotNone("first_name"). \
            checkNotNone("last_name"). \
            checkNotNone("password"). \
            checkEmail("email"). \
            checkNationalCode("national_code"). \
            checkPhone("phone_number")
        validator.\
            objectValidator. \
            checkNonDuplicateObject("username", User, username=data.get("username"))
        errors = validator.getValidatorsErrors()

        if validator.statusCode != 200:
            return Response(errors, status.HTTP_400_BAD_REQUEST)
        try:
            user = User(
                username=data.get("username"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                national_code=data.get("national_code"),
                phone_number=data.get("phone_number"),

            )
            user.set_password(raw_password=data.get("password"))
            with connection.cursor() as c:
                w = c.execute(
                    """
                    INSERT INTO auth_user (password, username, first_name, last_name, email, national_code, phone_number,is_superuser,is_staff,is_active) VALUES("{password}", "{username}","{first_name}","{last_name}","{email}", "{national_code}","{phone_number}",FALSE,FALSE,TRUE );
                     """.format(
                        username=data.get("username"),
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name"),
                        email=data.get("email"),
                        national_code=data.get("national_code"),
                        phone_number=data.get("phone_number"),
                        password=user.password
                    ))

            user = User.objects.get(username=data.get("username"))

        except:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        # qs_json = djserializers.serialize('json', [user])
        return Response(self.serializer_class(user).data)
        # return HttpResponse(qs_json, content_type='application/json')


class CategoryAPI(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BusinessAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Business.objects.all()
    serializer_class = BusinessSimpleSerializer


class ServiceAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class SansAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Sans.objects.all()
    serializer_class = SansSerializer


class ReserveAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer



class ReviewAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class TransactionAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class FileAPI(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer

