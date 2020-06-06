import json

from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Notification import NotificationController
from passlib.hash import pbkdf2_sha256  as decryptor
from API.models import Sans,Reserve,Service
import API.orm as orm
class ReserveController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        # try:
            user_id = request.GET['userId']
            data = request.POST
            description = data['description']
            sans_id = data['sans_id']
            service_id = data['service_id']
            date = data['date']
            sans = orm.select(Sans,id=sans_id)[0]
            verified = True

            # reserves = Reserve.objects.filter(sans_id=sans_id,
            #                                 date=date,
            #                                 service_id=service_id,
            #                                 is_cancelled=False).values()
            reserves = orm.select(Sans,sans_id=sans_id,date=date,service_id=service_id,is_cancelled=False)[0]
            free = len(reserves) == 0
            if free and verified:

                # reserve = Reserve.objects.create(user_id=user_id,
                #                                   description=description,
                #                                   sans_id=sans_id,
                #                                   date=date,
                #                                   service_id=service_id,
                #                                   )
                orm.insert(Reserve,user_id=user_id,
                                                  description=description,
                                                  sans_id=sans_id,
                                                  date=date,
                                                  service_id=service_id)
                return Response("DONE", status=status.HTTP_200_OK)
            else:
                raise Exception

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
