
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Business
import json
import API.orm as orm
class CategoryController(APIView):

    def get(self, request, format=None, *args, **kwargs):

        try:
            id = request.GET['category_id']
            business_data = orm.toDict(orm.select(Business,category_id=id))
            return Response(business_data, status= status.HTTP_200_OK)

        except Exception:
            return Response({}, status= status.HTTP_400_BAD_REQUEST)


   