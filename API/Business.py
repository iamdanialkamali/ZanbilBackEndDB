
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as restStatus

from .models import Business, BusinessFile, Service
import json
import API.orm as orm
from .validation import FieldValidator


class BusinessController(APIView):
    def put(self, request, format=None, *args, **kwargs):
            # user_id = tokenizer.meta_encode(request.META)
         # try:
            # user_id = tokenizer.meta_decode(request.META)
            try:
                user_id = request.GET['userId']
            except:
                return  Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
            validator = FieldValidator(request.data)
            validator.checkNotNone('name'). \
                checkNotNone('phone_number'). \
                checkNotNone('description'). \
                checkNotNone('category'). \
                validate()
            if validator.statusCode != 200:
                return Response({'status': False, 'errors': validator.getErrors()},status=validator.statusCode)
            data = request.data
            name = data['name']
            phone_number = data['phone_number']
            address = data['address']
            description = data['description']
            category = data['category']


            if(True):
                orm.insert(Business,
                    owner_id=user_id,
                    name=name,
                    phone_number=phone_number,
                    address=address,
                    description=description,
                    category_id=category,
                    score=0,
                )
                mybusiness = orm.select(Business,owner_id=user_id,name=name)[0]

            return Response({"business":orm.toDict(mybusiness),"pictures":orm.toDict(orm.select(BusinessFile,business_id=mybusiness.id))}, status=restStatus.HTTP_200_OK)

         # except Exception :
         #     return Response({},status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None, *args, **kwargs):

        # try:
            validator = FieldValidator(request.GET)
            validator.checkNotNone('business_id'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

            id = request.GET['business_id']
            mybusiness = orm.select(Business, id=id)[0]
            return Response(
                {
                    "business":orm.toDict(mybusiness),
                    "services":orm.toDict(orm.select(Service,business_id=mybusiness.id)),
                    "pictures":orm.toDict(orm.select(BusinessFile,business_id=mybusiness.id))
                }, status= restStatus.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None, *args, **kwargs):
         # try:
            validator = FieldValidator(request.data)
            validator.checkNotNone('name'). \
                checkNotNone('phone_number'). \
                checkNotNone('description'). \
                checkNotNone('category'). \
                checkNotNone('id'). \
                validate()
            if validator.statusCode != 200:
                return Response({'status': False, 'errors': validator.getErrors()},status=validator.statusCode)
            data = request.data
            name = data['name']
            phone_number = data['phone_number']
            address = data['address']
            description = data['description']
            category = data['category']
            id = data['id']

            if(True):
                status = orm.update(Business,id,
                           name=name,
                           phone_number=phone_number,
                           address=address,
                           description=description,
                           category_id=category
                           )

                if not status:
                     return Response({},status=restStatus.HTTP_400_BAD_REQUEST)
                mybusiness = orm.select(Business, id=id)[0]
                return Response(
                    {
                        "business": orm.toDict(mybusiness),
                        "pictures": orm.toDict(orm.select(BusinessFile, business_id=mybusiness.id))
                    }, status=restStatus.HTTP_200_OK)
         # except Exception :
         #     return Response({},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None, *args, **kwargs):

        # try:
            validator = FieldValidator(request.data)
            validator.checkNotNone('userId'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            id = request.data['userId']
            mybusiness = orm.select(Business, owner_id=id)

            data = []

            for business in mybusiness:
                data.append(
                    {
                        "business": orm.toDict(business),
                        "pictures": orm.toDict(orm.select(BusinessFile, business_id=business.id))
                    }
                )
            return Response(
                data, status= restStatus.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)



class BusinessSearchController(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # try:
            data = request.GET
            query = "SELECT \"API_business\".\"id\", \"API_business\".\"name\" , \"API_business\".\"score\", \"API_business\".\"owner_id\", \"API_category\".\"id\" as \"categoryId\", \"API_category\".\"name\" as \"categryName\", \"API_business\".\"address\", \"API_business\".\"phone_number\", \"API_business\".\"description\" FROM \"API_business\" INNER JOIN \"API_category\" ON (\"API_business\".\"category_id\" = \"API_category\".\"id\") WHERE ( 1=1"
            if data.get('business_name'):
                query += " AND \"API_business\".\"name\" LIKE  {}".format("'%" + data.get('business_name') + "%'")
            if data.get('category'):
                query += " AND \"API_category\".\"name\" LIKE  {}".format("'%" + data.get('category') + "%'")
            query += ") ORDER BY \"score\" DESC"

            res = orm.rawQuery(query)
            resDict = orm.toDict(res)
            return Response(resDict, status=restStatus.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
