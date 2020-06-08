
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Review,Service
import json
import API.orm as orm
from .validation import FieldValidator


class ReviewController(APIView):
    def put(self, request, format=None, *args, **kwargs):
         try:
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

            validator = FieldValidator(request.POST)
            validator.checkNotNone('name'). \
                checkType('point',float). \
                checkNotNone('description'). \
                checkNotNone('service_id'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

            data = request.POST
            point = float(data['point'])
            description = data['description']
            service_id = data['service_id']
            if 0 <= point <= 10 :
                self.newPointCalculator(service_id,point)
                orm.insert(Review,
                    user_id=user_id,
                    description=description,
                    service_id=service_id,
                    rating=point
                )
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_200_OK)

         except Exception :
             return Response({}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None, *args, **kwargs):

        # try:


        validator = FieldValidator(request.GET)
        validator.checkNotNone('business_id').\
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        id = request.GET['business_id']
        reviews = Review.objects.filter(service__business__id=id)

        review_datas = ReviewSerializer(reviews,many=True).data
        return Response(review_datas, status= status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)
    @staticmethod
    def newPointCalculator(service_id,point):
        service = Serviceobjects.get(pk=service_id)
        service.rating = (service.rating*service.review_count + point)/(service.review_count+1)
        service.review_count = service.review_count + 1
        service.save(force_update=True)
