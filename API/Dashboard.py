from django.db.models import Count
from khayyam import  JalaliDate,JalaliDatetime
from datetime import timedelta
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
            today = JalaliDate.today()
            # reserves = Reserve.objects.filter(service_business__id=business_id)
            #
            # business = Business.objects.get(pk=business_id)

            #find all reserves for today
            numReserveInDay=self.findAllReserveForADay(today,business_id)

            #find all reserves for yesterday
            yesterday = (JalaliDate.today()-timedelta(1)).__str__()
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
            upcomingReserve=self.getUpcomingReserve(today,business_id)

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
                    "date":reserve.date,
                    "startTime":sans.startTime,
                    "endTime":sans.endTime,
                    })
        allReserve=sorted(allReserve,key=lambda k: k['date'])
        return allReserve


    @staticmethod
    def getUpcomingReserve(day,business_id):
        upcomingReserve=[]
        services=orm.select(Service,business_id=business_id)
        now = JalaliDatetime.now()
        reserves = []
        for service in services:
            reserves += orm.select(Reserve,service_id=service.id)
        for reserve in reserves:
                sans = orm.select(Sans,id=reserve.sans_id)[0]
                splited_date = reserve.date.split('-')
                splited_time = sans.startTime.split(':')
                reserve_time = JalaliDatetime(
                    int(splited_date[0]),
                    int(splited_date[1]),
                    int(splited_date[2]),
                    int(splited_time[0]),
                    int(splited_time[1]),
                    0
                )

                if(reserve_time > now):
                    upcomingReserve.append(
                        orm.toDict(reserve)
                    )



        upcomingReserve=sorted(upcomingReserve,key=lambda k: k['date'])
        return upcomingReserve

    @staticmethod
    def findAllReserveForADay(day,business_id):
        services=orm.select(Service,business_id=business_id)
        reserves = []
        # print(day)
        for service in services:
            # currentMonthReserve = Reserve.objects.filter(service_id=service.id, date__contains=day)
            # # print(currentMonthReserve.query)
            # # q = Reserve.objects.raw("SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` WHERE (`API_reserve`.`date` LIKE BINARY %{}% AND `API_reserve`.`service_id` = {})".format(day.__str__(),service.id))
            try:
                query = "SELECT * FROM API_reserve WHERE date LIKE {} AND service_id={};".format('"%'+day.__str__()+'%"',service.id)
                reserves += orm.rawQuery(query)
            except:
                pass
        numReserveInDay=len(reserves)
        return numReserveInDay

    @staticmethod
    def findAllReserveForAMonth(day,business_id):
        day=day.__str__()
        # currentMonthReserve=Reserve.objects.filter(service__business__id=business_id , date__contains=day[:7])
        query = "SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` INNER JOIN `API_service` ON (`API_reserve`.`service_id` = `API_service`.`id`) WHERE (`API_reserve`.`date` LIKE  {} AND `API_service`.`business_id` ={})".format('"%'+day+'%"',business_id)
        numReserveInMonth=len(orm.rawQuery(query))
        return numReserveInMonth

    @staticmethod
    def  findAllReserveForAWeek(day,business_id):
        start_week_date = day - timedelta(days=JalaliDate.today().weekday())
        this_week_days_date = []
        weekday_date=start_week_date
        for i in range(7):
            this_week_days_date.append("'"+weekday_date.__str__()+"'")
            weekday_date = weekday_date + timedelta(1)
        # currentWeekReserve=Reserve.objects.filter(service__business__id=business_id , date__in=this_week_days_date)
        q = orm.rawQuery("SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` INNER JOIN `API_service` ON (`API_reserve`.`service_id` = `API_service`.`id`) WHERE (`API_reserve`.`date` IN ({}) AND `API_service`.`business_id`={})".format(", ".join(this_week_days_date), business_id))

        numReserveInWeek=len(q)
        return numReserveInWeek


    @staticmethod
    def findPopularService(day,business_id):
        popularService=[]
        services=orm.select(Service,business_id=business_id)
        for service in services:
            Tname=service.name
            dayS=day.__str__()
            query = "SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` WHERE (`API_reserve`.`date` LIKE BINARY {} AND `API_reserve`.`service_id` = {})".format('"%'+dayS[:7]+'%"', service.id)
            cMonthRes = orm.rawQuery(query)
            # cMonthRes=Reserve.objects.filter(service_id=service.id , date__contains=dayS[:7])
            # print(cMonthRes.query)
            TnumberOfReserveInCurrentMonth=len(cMonthRes)
            start_week_date = day - timedelta(days=JalaliDate.today().weekday())
            this_week_days_date = []
            weekday_date=start_week_date
            for i in range(7):
                this_week_days_date.append(weekday_date.__str__())
                weekday_date = weekday_date + timedelta(1)
            # cWeekRes=Reserve.objects.filter(service_id=service.id , date__in=this_week_days_date)
            cWeekRes = orm.rawQuery(
                "SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` WHERE (`API_reserve`.`date` IN ({}) AND `API_reserve`.`service_id` = {})".format(
                    ", ".join(this_week_days_date), service.id))

            TnumberOfReserveInCurrentWeek=len(cWeekRes)
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
        res = orm.rawQuery("SELECT `API_reserve`.`id`, `API_reserve`.`user_id`, `API_reserve`.`service_id`, `API_reserve`.`sans_id`, `API_reserve`.`description`, `API_reserve`.`date`, `API_reserve`.`isCancelled` FROM `API_reserve` INNER JOIN `API_service` ON (`API_reserve`.`service_id` = `API_service`.`id`) WHERE `API_service`.`business_id` = {}".format(business_id))
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


