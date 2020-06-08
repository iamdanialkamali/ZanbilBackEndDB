from khayyam import  JalaliDate
from datetime import timedelta
from .models import Sans,Reserve

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
    def getSansForPage(timetable_id,date):

        #calculate weekdays date of given date
        date_splited = date.split('/')
        Jdate = JalaliDate(int(date_splited[0]), int(date_splited[1]), int(date_splited[2]))
        start_week_date = Jdate - timedelta(days=Jdate.weekday())
        today_weekday = JalaliDate.today().weekday()
        # make a list of weekdays date in our format
        this_week_days_date = []
        weekday_date=start_week_date
        for i in range(7):
            this_week_days_date.append("'"+weekday_date.__str__().replace('/', '-')+"'")
            weekday_date = weekday_date + timedelta(1)

        #get sanses
        # selected_sanses = Sans.objects.filter(
        #     timetable__id=timetable_id)
        selected_sanses = orm.select(Sans,timeTable_id=timetable_id)

        # get reserved sanses in given week
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date)
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date)
        #exmine are seleted sanses reserved
        
        # reserved_sanses = Reserve.objects.filter(date__in=this_week_days_date,isCancelled=False).values('sans_id').annotate(total=Count('sans_id')).order_by('total')
        # reserved_sanses = orm.rawQuery("SELECT \"API_reserve\".\"sans_id\", COUNT(\"API_reserve\".\"sans_id\") AS \"total\" FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\"  IN ({})  AND \"API_reserve\".\"isCancelled\" = False) GROUP BY \"API_reserve\".\"sans_id\" ORDER BY \"total\" ASC".format(", ".join(this_week_days_date)))


        result=[[],[],[],[],[],[],[]]
        for sans in selected_sanses:
            is_reserved = False
            if(start_week_date < JalaliDate.today()-timedelta(today_weekday)):
                is_reserved = True

            elif(start_week_date == JalaliDate.today()-timedelta(today_weekday) and  sans.weekDay<today_weekday  ):
                is_reserved = True

            # capacity = 1
            # capacity = 1 - len(reserved_sanses.filter(sans_id = sans.id ).values())
            capacity = 1 - len(orm.rawQuery("SELECT \"API_reserve\".\"sans_id\", COUNT(\"API_reserve\".\"sans_id\") AS \"total\" FROM \"API_reserve\" WHERE (\"API_reserve\".\"date\" IN ({}) AND \"API_reserve\".\"isCancelled\" = False AND \"API_reserve\".\"sans_id\" = {}) GROUP BY \"API_reserve\".\"sans_id\" ORDER BY \"total\" ASC".format(", ".join(this_week_days_date),sans.id)))
            
            if(capacity<1):
                is_reserved = True
            result[sans.weekDay].append({"sans":orm.toDict(sans),"is_reserved": is_reserved , 'capacity':capacity})

        return (result,start_week_date.__str__().replace('-','/'))



