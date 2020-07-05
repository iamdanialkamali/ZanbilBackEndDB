import jdatetime
from django.db.models import Count
from khayyam import  JalaliDate,JalaliDatetime
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Review, Service, Sans, Reserve

from .models import Business,Service,Reserve,User
import API.orm as orm
from .validation import FieldValidator


class DashboardController(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # try:

            validator = FieldValidator(request.GET)
            validator.checkNotNone('id').\
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            business_id = request.GET['id']
            today = datetime.today()
            # reserves = Reserve.objects.filter(service_business__id=business_id)
            #
            # business = Business.objects.get(pk=business_id)

            #find all reserves for today
            numReserveInDay=self.findAllReserveForADay(today,business_id)

            #find all reserves for yesterday
            yesterday = today-timedelta(1)
            numReserveInYesterday=self.findAllReserveForADay(yesterday,business_id)

            #calculate increaseReservePercentageForDay
            increaseReservePercentageForDay=0
            if numReserveInYesterday!=0:
                increaseReservePercentageForDay = ((numReserveInDay-numReserveInYesterday)/numReserveInYesterday)*100
            else:
                increaseReservePercentageForDay = 100
            #find all reserves for current week
            numReserveInWeek=self.findAllReserveForAWeek(today,business_id)

            #find all reserves for last week
            numReserveInLastWeek=self.findAllReserveForAWeek(today-timedelta(7),business_id)

            #calculate increaseReservePercentageForWeek
            increaseReservePercentageForWeek=0
            if numReserveInLastWeek!=0:
                increaseReservePercentageForWeek=((numReserveInWeek-numReserveInLastWeek)/numReserveInLastWeek)*100
            else:
                increaseReservePercentageForWeek = 100
            #find all reserves for current mounth
            numReserveInMonth=self.findAllReserveForAMonth(today,business_id)

            #find all reserves for last mounth
            dayInLastMonth=today-timedelta(30)
            numReserveInLastMonth=self.findAllReserveForAMonth(dayInLastMonth,business_id)

            #calculate increaseReservePercentageForMonth
            increaseReservePercentageForMonth=0
            if numReserveInLastMonth!=0:
                increaseReservePercentageForMonth=((numReserveInMonth-numReserveInLastMonth)/numReserveInLastMonth)*100
            else:
                increaseReservePercentageForMonth = 100

            #find popularService
            popularService = self.findPopularService(today,business_id)

            #FIND upcoming reserves
            upcomingReserve=self.getUpcomingReserve(business_id)

            #  and all resrves
            allReserve=self.getAllReserve(business_id)

            #customers
            customers=self.findCustomers(business_id)


            return Response({
                    "increaseReservePercentageForWeek":increaseReservePercentageForWeek,
                    "increaseReservePercentageForMonth":increaseReservePercentageForMonth,
                    "increaseReservePercentageForDay":increaseReservePercentageForDay,
                    "customers":customers,
                    "allReservations":allReserve,
                    "upcomingReservations":upcomingReserve,
                    "popularService":popularService,
                    "numberOfReserveInDay":numReserveInDay,
                    "numberOfReserveInCurrentMonth":numReserveInMonth,
                    "numberOfReserveInCurrentWeek":numReserveInWeek,
                }, status= status.HTTP_200_OK)


        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def getAllReserve(business_id):
        allReserve=[]
        services=orm.select(Service,business_id=business_id)
        for service in services:
            reserves=orm.select(Reserve,service_id=service.id)
            for reserve in reserves:
                sans = orm.select(Sans, id=reserve.sans_id)[0]
                allReserve.append({
                    "serviceName":service.name,
                    "createdAt":reserve.createdAt,
                    "startTime":sans.startTime,
                    "endTime":sans.endTime
                       })
        allReserve=sorted(allReserve,key=lambda k: k['createdAt'])
        return allReserve


    @staticmethod
    def getUpcomingReserve(business_id):
        upcomingReserve=[]
        services=orm.select(Service,business_id=business_id)
        now = datetime.now()
        reserves = []
        for service in services:
            reserves += orm.select(Reserve,service_id=service.id)
        for reserve in reserves:
                sans = orm.select(Sans,id=reserve.sans_id)[0]
                reserve_time = datetime(
                    int(reserve.createdAt.year),
                    int(reserve.createdAt.month),
                    int(reserve.createdAt.day),
                    int(sans.startTime.hour),
                    int(sans.startTime.minute),

                    0
                )

                if(reserve_time > now):
                    upcomingReserve.append(
                        orm.toDict(reserve)
                    )



        upcomingReserve=sorted(upcomingReserve,key=lambda k: k['createdAt'])
        return upcomingReserve

    @staticmethod
    def findAllReserveForADay(day,business_id):
        services=orm.select(Service,business_id=business_id)
        reserves = 0
        # print(day)
        for service in services:
            # currentMonthReserve = Reserve.objects.filter(service_id=service.id, date__contains=day)
            # # print(currentMonthReserve.query)
            # # q = Reserve.objects.raw("SELECT \"API_reserve\".\"id\", \"API_reserve\".\"user_id\", \"API_reserve\".\"service_id\", \"API_reserve\".\"sans_id\", \"API_reserve\".\"description\", \"API_reserve\".\"date\", \"API_reserve\".\"isCancelled\" FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\" LIKE BINARY %{}% AND \"API_reserve\".\"service_id\" = {})".format(day.__str__(),service.id))
            try:
                query = "SELECT Count(*) FROM API_reserve WHERE \"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND service_id={};".format(day, day+timedelta(days=1), service.id)
                reserves += orm.rawQuery(query)[0].count
            except:
                pass
        numReserveInDay=reserves
        return numReserveInDay

    @staticmethod
    def findAllReserveForAMonth(day,business_id):
        # currentMonthReserve=Reserve.objects.filter(service__business__id=business_id , date__contains=day[:7])
        query = "SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" INNER JOIN \"API_service\" ON (\"API_reserve\".\"service_id\" = \"API_service\".\"id\") WHERE ( \"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND  \"business_id\" ={})".format(day,day+timedelta(days=30),business_id)
        numReserveInMonth= orm.rawQuery(query)[0].count
        return numReserveInMonth

    @staticmethod
    def findAllReserveForAWeek(date,business_id):
        start_week_date = (date - timedelta(days=jdatetime.datetime.fromgregorian(datetime=date).weekday())).replace(hour=0,minute=0,second=0)
        end_week_date = start_week_date + timedelta(days=7)
        # currentWeekReserve=Reserve.objects.filter(service__business__id=business_id , date__in=this_week_days_date)
        q = orm.rawQuery("SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" INNER JOIN \"API_service\" ON (\"API_reserve\".\"service_id\" = \"API_service\".\"id\") WHERE ( \"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND \"business_id\"={})".format(start_week_date,end_week_date, business_id))
        numReserveInWeek=q[0].count
        return numReserveInWeek


    @staticmethod
    def findPopularService(day,business_id):
        popularService=[]
        services=orm.select(Service,business_id=business_id)
        for service in services:
            Tname=service.name
            query = "SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" WHERE ( \"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND \"API_reserve\".\"service_id\" = {})".format(day,day+timedelta(days=30), service.id)
            cMonthRes = orm.rawQuery(query)
            # cMonthRes=Reserve.objects.filter(service_id=service.id , date__contains=dayS[:7])
            # print(cMonthRes.query)
            TnumberOfReserveInCurrentMonth=cMonthRes[0].count
            start_week_date = day - timedelta(days=JalaliDate.today().weekday())
            end_week_date = start_week_date + timedelta(days=7)

            query = "SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" WHERE (\"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND \"API_reserve\".\"service_id\" = {})".format(start_week_date,end_week_date, service.id)
            cWeekRes = orm.rawQuery(query)

            # cWeekRes = orm.rawQuery(
            #     "SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\" IN ( {} ) AND \"API_reserve\".\"service_id\" = {})".format(
            #         ", ".join(this_week_days_date), service.id))
            # print(cWeekRes)
            # cWeekRes = Reserve.objects.raw("SELECT COUNT(\"API_reserve\".\"id\") FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\" = ANY (\{ {} \}) AND \"API_reserve\".\"service_id\" = {})".format(
            #         ", ".join(this_week_days_date), service.id))
            TnumberOfReserveInCurrentWeek=cWeekRes[0].count
            popularService.append({
                    "name":Tname,
                    "numberOfReserveInCurrentMonth":TnumberOfReserveInCurrentMonth,
                    "TnumberOfReserveInCurrentWeek":TnumberOfReserveInCurrentWeek
                })
            popularService = sorted(popularService, key=lambda k: k['numberOfReserveInCurrentMonth'],reverse=True)
        return popularService[0:3]

    @staticmethod
    def findCustomers(business_id):
        customers=[]
        # customers_ids=Reserve.objects.filter(service__business__id=business_id).values_list('user', flat=True)
        res = orm.rawQuery("SELECT \"API_reserve\".\"id\", \"API_reserve\".\"user_id\", \"API_reserve\".\"service_id\", \"API_reserve\".\"sans_id\", \"API_reserve\".\"description\", \"API_reserve\".\"createdAt\", \"API_reserve\".\"isCancelled\" FROM \"API_reserve\" INNER JOIN \"API_service\" ON (\"API_reserve\".\"service_id\" = \"API_service\".\"id\") WHERE \"business_id\" = {}".format(business_id))
        customers_ids = [x.user_id for x in res]
        customers_ids=set(customers_ids)
        for id in customers_ids:
            customer=orm.select(User,id=id)[0]
            customers.append(
                {
                    "firstname":customer.first_name,
                    "lastname":customer.last_name,
                    "Email":customer.email,
                    "phone_number":customer.phone_number
                }
            )
        return customers


