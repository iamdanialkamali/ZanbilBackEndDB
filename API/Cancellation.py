import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reserve, Sans, Service
import json
from khayyam import *
import API.orm as orm

#cancel the reserve if its not too late
from .validation import FieldValidator


class CancellationController(APIView):
    def post(self, request, format=None, *args, **kwargs):
        # try:
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
            data = request.data

            validator = FieldValidator(request.data)
            validator.checkNotNone('reserve_id').\
                validate()
            if validator.statusCode != 200:
                return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            reserve_id = data['reserve_id']


            if(True):
                selected_Reserve = orm.select(Reserve,id=int(reserve_id))[0]
                if int(user_id) != selected_Reserve.user_id:
                    return Response({"its not your reservation"}, status=status.HTTP_403_FORBIDDEN)

                reserveDate=selected_Reserve.createdAt
                # sans = orm.select(Sans,id=selected_Reserve.sans_id)[0]
                # reserveTime=sans.startTime.split(":");
                # reserveDateTime=JalaliDatetime(int(reserveDate[0]),int(reserveDate[1]),int(reserveDate[2]), int(reserveTime[0]), int(reserveTime[1]),0);

                #find cancellation range
                service = orm.select(Service,id=selected_Reserve.service_id)[0]

                duration = service.cancellation_range
                delta = datetime.timedelta(minutes=int(duration))

                if(datetime.datetime.now()+delta < selected_Reserve.createdAt and  not selected_Reserve.isCancelled):
                    orm.update(Reserve,selected_Reserve.id,isCancelled=True)
                    return Response({"message":"done!"}, status=status.HTTP_200_OK)
                elif(selected_Reserve.isCancelled):
                    return Response({"message":"قبلا کنسل شده است."}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"message":"برای کنسل کردن دیر شده است."}, status=status.HTTP_400_BAD_REQUEST)

        # except Exception :
        #     return Response({},status=status.HTTP_400_BAD_REQUEST)
