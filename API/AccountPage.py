
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review, User, Reserve, Business, User, Sans, Service
from khayyam import *
import datetime
import API.orm as orm
import hashlib
class AccountPageController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        try:
            user_id = request.GET['userId']
            reserves = orm.select(Reserve,user_id=user_id)
            reserves_list = []
            for reserve in reserves:
                sans = orm.select(Sans, id=reserve.sans_id)[0]
                service = orm.select(Service,id=reserve.service_id)[0]
                if(reserve.date[4]=="/"):
                    reserveDate=reserve.date.split("/");
                else:
                    reserveDate=reserve.date.split("-");
               
                reserveTime=sans.startTime.split(":");
                
                reserveDateTime=JalaliDatetime(int(reserveDate[0]),int(reserveDate[1]),int(reserveDate[2]), int(reserveTime[0]), int(reserveTime[1]),0)

                #find cancellation range
                duration = service.cancellation_range.split(":")
                delta = datetime.timedelta(hours=int(duration[0])-1, minutes=int(duration[1]))

                #check isn't it late
                if(JalaliDatetime.now() + delta < reserveDateTime):
                    reserve = {
                        # 'reserve':ReserveSerializer(reserve).data,
                        'reserve':reserve,
                        'is_cancellabe':True
                    }
                else:
                    reserve = {
                        'reserve':reserve,
                        'is_cancellabe':False
                    }
                    reserves_list.append(reserve)


            user = orm.select(User,id=user_id)
            businseses = orm.select(Business, owner_id=user_id)

            return Response({
                        'user':orm.toDict(user[0]),
                        'reserves': orm.toDict(reserves_list),
                        'businseses':orm.toDict(businseses)

                    }, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, format=None, *args, **kwargs):
        try:
            user_name = request.POST.get("username")
            first_name= request.POST.get("firstName")
            last_name= request.POST.get("lastName")
            password= request.POST.get("password")
            email= request.POST.get("email")
            national_code= request.POST.get("nationalCode")
            phone_number= request.POST.get("phoneNumber")
            try:
                orm.insert(User,
                           username=user_name,
                           last_name=last_name,
                           first_name=first_name,
                           password=hashlib.sha256(password.encode()).hexdigest().__str__(),
                           email=email,
                           national_code=national_code,
                           phone_number=phone_number,
                           is_superuser=False,
                           is_staff=False,
                           is_active=True
                           )
            except:
                return Response({
                    'user': "نام کاربری تکراری است"
                }, status=status.HTTP_200_OK)
            user = orm.select(User,username=user_name)
            return Response({
                'user': orm.toDict(user[0])
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        try:
            user_name = request.POST.get("username")
            password= request.POST.get("password")
            user = orm.select(User,username=user_name,password=hashlib.sha256(password.encode()).hexdigest().__str__())
            if len(user)>0:
                userDict = orm.toDict(user[0])
                del userDict['password']
                return Response({
                    'user': userDict
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)