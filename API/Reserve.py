import json
from datetime import datetime

import jdatetime
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
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
            data = request.data
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
            reserves = orm.select(Reserve,sans_id=sans_id,date=date,service_id=service_id,isCancelled=False)
            free = len(reserves) == 0
            if free and verified:

                # reserve = Reserve.objects.create(user_id=user_id,
                #                                   description=description,
                #                                   sans_id=sans_id,
                #                                   date=date,
                #                                   service_id=service_id,
                #                                   )
                year,month,day =map(int,date.split("-"))
                orm.insert(Reserve,user_id=user_id,
                                                  description=description,
                                                  sans_id=sans_id,
                                                  date=date,
                                                  createdAt="\""+jdatetime.datetime(
                                                      year=year,
                                                      month=month,
                                                      day=day,
                                                      hour=sans.startTimeHour,
                                                      minute=sans.startTimeMinute
                                                  ).togregorian().__str__() + "\"",
                                                  service_id=service_id
                           ,isCancelled=False)
                return Response("DONE", status=status.HTTP_200_OK)
            else:
                raise Exception

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
