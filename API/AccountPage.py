
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review, User, Reserve, Business, User, Sans, Service
from khayyam import *
import datetime
import API.orm as orm
import hashlib

from .validation import FieldValidator


class AccountPageController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        # try:
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
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
        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, format=None, *args, **kwargs):
        # try:
            user_name = request.data.get("username")
            first_name= request.data.get("firstName")
            last_name= request.data.get("lastName")
            password= request.data.get("password")
            email= request.data.get("email")
            national_code= request.data.get("nationalCode")
            phone_number= request.data.get("phoneNumber")
            validator = FieldValidator(request.data)
            validator.checkNotNone('username'). \
                checkNotNone('description'). \
                checkNotNone('firstName'). \
                checkNotNone('lastName'). \
                checkNotNone('password'). \
                checkEmail('email'). \
                checkNationalCode('nationalCode'). \
                checkPhone('phoneNumber'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            # try:
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
            # except:
            #     return Response({
            #         'user': "نام کاربری تکراری است"
            #     }, status=status.HTTP_200_OK)
            user = orm.select(User,username=user_name)
            return Response({
                'user': orm.toDict(user[0])
            }, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        # try:
            user_name = request.data.get("username")
            password= request.data.get("password")
            validator = FieldValidator(request.data)
            validator.checkNotNone('username'). \
                checkNotNone('password'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
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
        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)