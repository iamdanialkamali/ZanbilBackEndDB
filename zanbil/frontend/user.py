import json
from django.core import serializers
from django.http import HttpResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from zanbil.models import User
from django.contrib.auth.hashers import make_password
from zanbil.serializer import UserSerializer
from zanbil.validation import FieldValidator, DataValidator, ObjectValidator
from django.db import connection
cursor = connection.cursor()
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



class UserAPI(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    required_alternate_scopes = {
        "GET": [["read"]],
        "POST": [["create"]],
        "PUT": [["update"]],
        "DELETE": [["delete"]],
    }

    def get(self, request, format=None):
        users = User.objects.raw("SELECT id,username FROM auth_user")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def put(self, request, format=None):
        data = request.data
        validator = DataValidator(data)
        validator.\
            fieldValidator.\
            checkNotNone("username"). \
            checkNotNone("first_name"). \
            checkNotNone("last_name"). \
            checkNotNone("password"). \
            checkEmail("email"). \
            checkNationalCode("national_code"). \
            checkPhone("phone_number")
        validator.\
            objectValidator.\
            checkNonDuplicateObject("username",User,username=data.get("username"))
        errors = validator.getValidatorsErrors()
        if validator.statusCode != 200:
            return Response(errors,status.HTTP_400_BAD_REQUEST)
        try:
            with connection.cursor() as c:
                w = c.execute(
                    """INSERT INTO auth_user (password, username, first_name, last_name, email, national_code, phone_number,is_superuser,is_staff,is_active) VALUES("{password}", "{username}","{first_name}","{last_name}","{email}", "{national_code}","{phone_number}",FALSE,FALSE,TRUE );""".format(
                        username=data.get("username"),
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name"),
                        email=data.get("email"),
                        national_code=data.get("national_code"),
                        phone_number=data.get("phone_number"),
                        password=make_password(data.get("password"))
                    ))

            user = User.objects.get(username=data.get("username"))

        except:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        qs_json = serializers.serialize('json',[user])
        return HttpResponse(qs_json, content_type='application/json')


