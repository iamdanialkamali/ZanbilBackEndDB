import json
from datetime import datetime

from khayyam import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .Sans import SansController
from .TimeTable import TimeTableController
from rest_framework.parsers import MultiPartParser
from API.models import Sans, Service, ServiceFile, TimeTable
import API.orm as orm
from .validation import FieldValidator


class ServiceController(APIView):
    #

    def put(self, request, format=None, *args, **kwargs):

        # try:
        from ast import literal_eval
        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

        validator = FieldValidator(request.data)
        validator.checkNotNone('name'). \
            checkNotNone('description'). \
            checkNotNone('price'). \
            checkNotNone('business_id'). \
            checkNotNone('address'). \
            checkNotNone('days'). \
            checkNotNone('cancellation_range'). \
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        data = request.data
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        business_id = data.get('business_id')
        address = data.get('address')
        days = data.get('days')
        cancellation_range = data.get('cancellation_range')
        timetable = TimeTableController.buildTimetable(days, business_id)

        if (True):
            orm.insert(Service,
                       name=name,
                       description=description,
                       fee=price,
                       business_id=business_id,
                       rating=10,
                       address=address,
                       timeTable_id=timetable.id,
                       cancellation_range=cancellation_range
                       )
            myService = orm.select(Service,
                                   name=name,
                                   description=description,
                                   fee=price,
                                   business_id=business_id
                                   )[-1]

        sanses = SansController.getSansForWeek(timetable.id)

        return Response({
            'service': orm.toDict(myService),
            'timetable': sanses,
            "pictures": orm.toDict(orm.select(ServiceFile, service_id=myService.id))
        }
            , status=status.HTTP_200_OK)

    # except Exception :
    #     return Response({},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, *args, **kwargs):
        # try:
        validator = FieldValidator(request.GET)
        validator.checkNotNone('service_id'). \
            validate()
        id = request.GET['service_id']
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        service = orm.select(Service, id=id)[0]
        service_data = orm.toDict(service)
        timeTable = orm.select(TimeTable, id=service.timeTable_id)[0]


        today = JalaliDate.today().__str__().replace('-', '/')
        if request.GET.get('date'):
            today = JalaliDate.fromtimestamp(float(request.GET.get('date'))).__str__().replace('-', '/')#datetime.fromtimestamp(float(request.GET.get('date')))
        print(today)
        sanses, start_of_week_date = SansController.getSansForPage(timeTable_id=timeTable.id, date=today)

        return Response({"service": service_data,
                         "sanses": sanses,
                         "pictures": orm.toDict(orm.select(ServiceFile, service_id=service.id)),

                         "start_of_week_date": start_of_week_date},
                        status=status.HTTP_200_OK)

    # except Exception:
    #    return Response({}, status= status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        try:

            validator = FieldValidator(request.data)
            validator.checkNotNone('date'). \
                checkNotNone('service_id'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

            data = request.data
            date = data['date']
            id = data['service_id']
            service = orm.select(Service, id=id)[0]
            service_data = orm.toDict(service)

            timetable = orm.insert(TimeTable, services_id=service.id)
            (sanses, start_of_week_date) = SansController.getSansForPage(timeTable_id=timetable.id, date=date)

            return Response({"service": service_data,
                             "sanses": sanses,
                             "pictures": orm.toDict(orm.select(ServiceFile, service_id=service.id)),
                             "start_of_week_date": start_of_week_date}
                            , status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None, *args, **kwargs):

        try:
            from ast import literal_eval
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
            data = request.data
            name = data.get('name')
            id = data.get('id')
            description = data.get('description')
            fee = data.get('price')
            address = data.get('address')
            sanses = data.get('sanses')
            cancellation_range = data.get('cancellation_range')

            validator = FieldValidator(request.data)
            validator.checkNotNone('name'). \
                checkNotNone('description'). \
                checkNotNone('price'). \
                checkNotNone('id'). \
                checkNotNone('address'). \
                checkNotNone('sanses'). \
                checkNotNone('cancellation_range'). \
                validate()
            if validator.statusCode != 200:
                Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
            # edit name and fee and description
            selectedService = orm.toDict(orm.select(Service, id=id)[0])

            selectedService['name'] = name
            selectedService['fee'] = fee
            selectedService['address'] = address
            selectedService['cancellation_range'] = cancellation_range
            selectedService['description'] = description
            del selectedService['id']
            orm.update(Service, id, **selectedService)

            # edit sanses
            for sans in sanses:
                selectedSans = orm.select(Sans, id=int(sans['sans_id']))
                if sans.get('is_deleted') == "1":
                    orm.delete(Sans, id=sans['sans_id'])
                else:

                    if not (orm.update(Sans, id=sans['sans_id'],
                                       weekDay=sans['weekday'],
                                       startTimeHour=int(sans['startTime'][:2]),
                                       startTimeMinute=int(sans['startTime'][3:]),
                                       endTimeHour=int(sans['endTime'][:2]),
                                       endTimeMinute=int(sans['endTime'][3:]))):
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, *args, **kwargs):

        # try:
            from ast import literal_eval
            data = request.data
            id = data.get('id')
            orm.delete(Service, id=id)
            return Response({}, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SearchController(APIView):
    def post(self, request, format=None, *args, **kwargs):
        # try:
            query = "SELECT \"API_service\".\"id\", \"business_id\", \"API_service\".\"timeTable_id\", \"API_service\".\"name\", \"API_service\".\"address\", \"API_service\".\"fee\", \"API_service\".\"rating\", \"API_service\".\"description\", \"API_service\".\"cancellation_range\" FROM \"API_service\" INNER JOIN \"API_business\" ON (\"API_service\".\"business_id\" = \"API_business\".\"id\") INNER JOIN \"API_category\" ON (\"API_business\".\"category_id\" = \"API_category\".\"id\") WHERE ( 1=1"
            data = request.GET
            if data.get("service_name"):
                query += " AND \"API_service\".\"name\" LIKE  {}".format("'%" + data.get("service_name") + "%'")
            if data.get('business_name'):
                query += " AND \"API_business\".\"name\" LIKE  {}".format("'%" + data.get('business_name') + "%'")
            if data.get("min_price"):
                query += " AND \"fee\" <= {}".format(data.get("max_price"))
            if data.get("max_price"):
                query += " AND \"fee\" >= {}".format(data.get("max_price"))
            if data.get('category'):
                query += " AND \"API_category\".\"name\" LIKE  {}".format("'%" + data.get('category') + "%'")
            query += ") ORDER BY \"rating\" DESC"
            if data.get("sort_fee"):
                query += ",\"fee\" DESC"
            res = orm.rawQuery(query)
            resDict = orm.toDict(res)
            return Response(resDict, status=status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
