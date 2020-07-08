from django.db import connection
cursor = connection.cursor()
import re

from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def toDict(data):
    if isinstance(data,list):
        return [x._asdict() for x in data]
    return data._asdict()
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def select(model,**options):
    # query = "1 = 1 "
    # for key,value in options.items():
    #     query += "AND {}={} ".format(key,value)
    # x = model.objects.raw("select * from API_{} where {};".format(model.__name__.lower(),query))
    # y = serializer(x,many=True)
    # return y.data
    checkForSqlInjection(*list(options.values()))
    with connection.cursor() as c:
        query = "1 = 1 "
        for key, value in options.items():
            if isinstance(value,str):
                options[key] = "'"+ value +"'"
            else:
                options[key] = str(value)
        for key,value in options.items():
            if "__gt" in key:
                print("WTF")
            else:
                query += "AND \"{}\"={} ".format(key,value)
        modelName = "API_{}".format(model.__name__.lower()) if model.__name__.lower() != "user" else "auth_user"
        c.execute("select * from \"{}\" where {};".format(modelName,query))
        return namedtuplefetchall(c)

def insert(model,**options):
    checkForSqlInjection(*list(options.values()))
    with connection.cursor() as c:
        for key, value in options.items():
            if isinstance(value,str):
                options[key] = "'"+ value +"'"
            else:
                options[key] = str(value)
        keys = []
        modelName = "API_{}".format(model.__name__.lower()) if model.__name__.lower() != "user" else "auth_user"
        for x in options.keys():
            # keys.append("\"{}\".\"{}\"".format(modelName,x))
            keys.append("\"{}\"".format(x))
        query = "INSERT INTO \"{}\"({})  VALUES ({} );".format(modelName ,",".join(keys),",".join(options.values()))
        w = c.execute(query)

def delete(model,**options):
    checkForSqlInjection(*list(options.values()))
    with connection.cursor() as c:
        query = "1 = 1 "
        for key, value in options.items():
            if isinstance(value,str):
                options[key] = "'"+ value +"'"
            else:
                options[key] = str(value)
        for key,value in options.items():
            if "__gt" in key:
                print("WTF")
            else:
                query += "AND \"{}\"={} ".format(key,value)
        modelName = "API_{}".format(model.__name__.lower()) if model.__name__.lower() != "user" else "auth_user"
        c.execute("delete from \"{}\" where {};".format(modelName,query))
        return namedtuplefetchall(c)
def update(model,id,**options):
    # try:
        checkForSqlInjection(id,*list(options.values()))
        with connection.cursor() as c:
            query =  " "
            for key, value in options.items():
                if isinstance(value,str):
                    options[key] = "'"+ value +"'"
                else:
                    options[key] = str(value)
            for key,value in options.items():
                query += "\"{}\"={},".format(key,value)
            modelName = "API_{}".format(model.__name__.lower()) if model.__name__.lower() != "user" else "auth_user"
            final = "UPDATE \"{}\" SET {}  where id={};".format(modelName,query[:-1],id)
            c.execute(final)
            return True
    # except:
        # return False

def rawQuery(query):
    with connection.cursor() as c:
        c.execute(query)
        return namedtuplefetchall(c)


def calculateNewPoint(serviceId,point):
    with connection.cursor() as cursor:
        cursor.execute("CALL calculateNewPoint({},{})".format(serviceId,point))
    #     cursor.callproc('calculateNewPoint', [serviceId, point])

def checkForSqlInjection(*params):
    import django.core.exceptions
    for param in params:
        if ";" in param or " and " in param.lower() or " or " in param.lower() or "|" in param.lower() or "&" in param.lower():
            raise django.core.exceptions.ValidationError("{} اشتباه است.".format(param))

