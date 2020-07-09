import json
from datetime import datetime

import jdatetime
from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Notification import NotificationController
from passlib.hash import pbkdf2_sha256  as decryptor
from API.models import Sans,Reserve,Service, Transaction
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

            service = orm.select(Service,id=service_id)[0]
            year, month, day = map(int, date.split("-"))

            createdAt = datetime(
                      year=year,
                      month=month,
                      day=day,
                      hour=sans.startTime.hour,
                      minute=sans.startTime.minute,
                  )

            if createdAt < datetime.now():
                return Response({"message": "از تاریخ مجاز رزرو گذشته است."}, status=status.HTTP_400_BAD_REQUEST)

            reserves = orm.select(Reserve,sans_id=sans_id, createdAt="\""+createdAt.__str__() + "\"",service_id=service_id,isCancelled=False)

            verified = jdatetime.datetime.fromgregorian(datetime=createdAt).weekday() == sans.weekDay

            if not verified:
                return Response({"message":"تاریخ با سانس آن همخوانی ندارد."}, status=status.HTTP_400_BAD_REQUEST)

            free = len(reserves) == 0
            if free:
                orm.insert(Reserve,user_id=user_id,
                                                  description=description,
                                                  sans_id=sans_id,
                                                  # date=date,
                                                  createdAt="\""+createdAt.__str__() + "\"",
                                                  service_id=service_id
                           ,isCancelled=False)
                reserve = orm.select(Reserve,sans_id=sans_id, createdAt=createdAt.__str__(),service_id=service_id,isCancelled=False)[0]
                if service.fee > 0:
                    orm.insert(Transaction,reserve_id=reserve.id,paidAt="\""+createdAt.__str__() + "\"",amount=service.fee)
                return Response("DONE", status=status.HTTP_200_OK)
            else:
                return Response({"message":"قبلا رزرو شده است."}, status=status.HTTP_400_BAD_REQUEST)

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
