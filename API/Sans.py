from datetime import timedelta
from .models import Sans,Reserve
import jdatetime
from django.db.models import Count

import API.orm as orm
class SansController:
    @staticmethod
    def getSansForWeek(timetable_id):
        sanses = orm.select(Sans,timeTable_id=timetable_id)
        result = [[],[],[],[],[],[],[]]
        for sans in orm.toDict(sanses) :
            result[sans['weekDay']].append(sans)
        return result

    # get date and timetable id and return sanses
    @staticmethod
    def getSansForPage(timeTable_id,date):

        #calculate weekdays date of given date


        start_week_date = (date - timedelta(days=jdatetime.datetime.fromgregorian(datetime=date).weekday())).replace(hour=0,minute=0,second=0)
        end_week_date = start_week_date + timedelta(days=7)
        today_weekday = jdatetime.datetime.today().weekday()
        # make a list of weekdays date in our format
        this_week_days_date = []
        weekday_date=start_week_date
        for i in range(7):
            this_week_days_date.append("\"{}\"".format(weekday_date.__str__()))
            weekday_date = weekday_date + timedelta(1)

        #get sanses
        # selected_sanses = Sans.objects.filter(
        #     timetable__id=timetable_id)
        selected_sanses = orm.select(Sans,timeTable_id=timeTable_id)

        # get reserved sanses in given week
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date)
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date)
        #exmine are seleted sanses reserved
        
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date,isCancelled=False).values('sans_id').annotate(total=Count('sans_id')).order_by('total')
        # reserved_sanses = orm.rawQuery("SELECT \"API_reserve\".\"sans_id\", COUNT(\"API_reserve\".\"sans_id\") AS \"total\" FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\"  IN ({})  AND \"API_reserve\".\"isCancelled\" = False) GROUP BY \"API_reserve\".\"sans_id\" ORDER BY \"total\" ASC".format(", ".join(this_week_days_date)))


        result=[[],[],[],[],[],[],[]]
        for sans in selected_sanses:
            is_reserved = False
            if(start_week_date < jdatetime.datetime.today()-timedelta(today_weekday)):
                is_reserved = True

            elif(start_week_date == jdatetime.datetime.today()-timedelta(today_weekday) and  sans.weekDay<today_weekday  ):
                is_reserved = True

            query = "SELECT \"API_reserve\".\"id\" FROM \"API_reserve\" WHERE (\"API_reserve\".\"createdAt\" >= \'{}\' AND \"API_reserve\".\"createdAt\" <=  \'{}\' AND \"API_reserve\".\"sans_id\" = {} )".format(start_week_date,end_week_date, sans.id)
            c = orm.rawQuery(query)
            capacity = 1 - len(c)
            if(capacity==0):
                result[sans.weekDay].append({"sans":orm.toDict(sans),"is_reserved": True , 'capacity':0 ,'reserveId':c[0].id})
            else:
                result[sans.weekDay].append({"sans":orm.toDict(sans),"is_reserved": False , 'capacity':capacity})

        return (result,start_week_date.__str__().replace('-','/'))



