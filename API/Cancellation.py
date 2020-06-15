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
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            reserve_id = data['reserve_id']


            if(True):
                selected_Reserve = orm.select(Reserve,id=int(reserve_id))[0]
                if int(user_id) != selected_Reserve.user_id:
                    return Response({"its not your reservation"}, status=status.HTTP_403_FORBIDDEN)

                #find reservation dateTime
                if(selected_Reserve.date[4]=="/"):
                    reserveDate=selected_Reserve.date.split("/");
                else:
                    reserveDate=selected_Reserve.date.split("-");
                # sans = orm.select(Sans,id=selected_Reserve.sans_id)[0]
                # reserveTime=sans.startTime.split(":");
                # reserveDateTime=JalaliDatetime(int(reserveDate[0]),int(reserveDate[1]),int(reserveDate[2]), int(reserveTime[0]), int(reserveTime[1]),0);

                #find cancellation range
                service = orm.select(Service,id=selected_Reserve.service_id)[0]

                duration = service.cancellation_range
                delta = datetime.timedelta(minutes=int(duration))

                if((datetime.datetime.now().replace(tzinfo=None)+delta) < selected_Reserve.createdAt.replace(tzinfo=None)):
                    orm.update(Reserve,selected_Reserve.id,is_cancelled=True)
                    return Response({"done!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"its too late for cancellation"}, status=status.HTTP_400_BAD_REQUEST)

        # except Exception :
        #     return Response({},status=status.HTTP_400_BAD_REQUEST)
