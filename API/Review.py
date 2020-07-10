
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Review,Service,Reserve
import json
import API.orm as orm
from .validation import FieldValidator
from django.db import connection
connectionDict = {}

class ReviewController(APIView):
    def put(self, request, format=None, *args, **kwargs):
         # try:
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

            validator = FieldValidator(request.data)
            validator.\
                checkNotNone('point'). \
                checkNotNone('description'). \
                checkNotNone('reserve_id'). \
                validate()
            if validator.statusCode != 200:
                return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

            data = request.data
            point = int(data['point'])
            description = data['description']
            reserve_id = data['reserve_id']
            reserves = orm.select(Reserve,id=reserve_id,user_id=user_id)
            if len(reserves) == 0:
                return Response({"message":".رزرو وجود ندارد"},status.HTTP_404_NOT_FOUND)
            reserve = reserves[0]
            # if len(orm.select(Review,reserve_id=reserve.id)) >0:
            #     return Response({"message":"قبلا نظر ثبت شده است."},status.HTTP_400_BAD_REQUEST)

            if 0 <= point <= 10:
                # newPointCalculator(reserve.service_id,point)
                orm.calculateNewPoint(reserve.service_id,point)
                orm.insert(Review,
                    description=description,
                    reserve_id=reserve.id,
                    rating=point
                )
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_200_OK)

         # except Exception :
         #     return Response({}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None, *args, **kwargs):

        # try:

        global connectionDict
        validator = FieldValidator(request.GET)
        validator.\
            checkNotNone('service_id').\
            checkNotNone('page').\
            checkNotNone('size').\
            validate()
        if validator.statusCode != 200:
            return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        id = request.GET['service_id']
        orm.checkForSqlInjection(id)
        size = int(request.GET['size'])
        page = int(request.GET['page'])
        # if not connectionDict.get(token,False):
        #     connectionDict[token] = connection.cursor()
        #     connectionDict[token].execute("SELECT \"API_review\".\"id\", \"API_review\".\"description\", \"API_review\".\"rating\", \"API_review\".\"reserve_id\" FROM \"API_review\" INNER JOIN \"API_reserve\" ON (\"API_review\".\"reserve_id\" = \"API_reserve\".\"id\") WHERE \"API_reserve\".\"service_id\" = {}".format(id))
        # try:
        #     w = connectionDict[token].fetchone()
        #     if w is None:
        #         raise Exception
        # except:
        #     del connectionDict[token]
        #     return Response({"message":"تمام شد."}, status= status.HTTP_404_NOT_FOUND)
        data = []
        try:
            cur = connection.cursor()
            cur.execute("SELECT \"API_review\".\"id\", \"API_review\".\"description\", \"API_review\".\"rating\", \"API_review\".\"reserve_id\" FROM \"API_review\" INNER JOIN \"API_reserve\" ON (\"API_review\".\"reserve_id\" = \"API_reserve\".\"id\") WHERE \"API_reserve\".\"service_id\" = {}".format(id))
            for i in range(page*size):
                cur.fetchone()
            for i in range(size):
                d = cur.fetchone()
                if d:
                    data.append(d)
        except:
            if len(data) == 0:
                return Response({"message":"تمام شد."}, status= status.HTTP_404_NOT_FOUND)
        columns = [col[0] for col in cur.description]
        reserve = [dict(zip(columns, w)) for w in data]

        # reviews = Review.objects.filter(reserve__service_id=id)
        # review_datas = ReviewSerializer(reviews,many=True).data
        # return Response(orm.toDict(reviews), status= status.HTTP_200_OK)
        return Response(reserve, status= status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)
    # @staticmethod
    # def newPointCalculator(service_id,point):
        # service = orm.select(Service,id=service_id)[0]
        #
        #
        # orm.update(Service,id=service_id,rating=)
        # service.rating = (service.rating*service.reviewCount + point)/(service.reviewCount+1)
        # service.review_count = service.review_count + 1
        # service.save(force_update=True)
