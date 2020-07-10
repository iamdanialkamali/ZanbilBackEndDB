from datetime import datetime, date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Review, Service, Reserve, Wallet, Transaction
import json
import API.orm as orm
from .validation import FieldValidator
from django.db import connection

class WalletController(APIView):
    def put(self, request, format=None, *args, **kwargs):
         # try:
            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

            validator = FieldValidator(request.data)
            validator.\
                checkNotNone('name'). \
                validate()
            if validator.statusCode != 200:
                return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

            data = request.data
            name = data['name']
            if len(orm.select(Wallet,user_id=user_id,name=name)) != 0:
                return Response({"message":"کیف پول وجود دارد."},status.HTTP_400_BAD_REQUEST)
            orm.insert(Wallet,name=name,user_id=user_id,credit=0)

            return Response(orm.toDict(orm.select(Wallet,user_id=user_id,name=name)), status=status.HTTP_200_OK)

         # except Exception :
         #     return Response({}, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request, format=None, *args, **kwargs):

        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors': "AUTHENTICATION ERROR"}, status=403)

        userWallets = orm.toDict(orm.select(Wallet,user_id=user_id))
        return Response(userWallets, status= status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors': "AUTHENTICATION ERROR"}, status=403)
        validator = FieldValidator(request.data)
        validator. \
            checkNotNone('walletId'). \
            checkNotNone('amount'). \
            validate()
        if validator.statusCode != 200:
            return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
        walletId = request.data.get("walletId")
        amount = request.data.get("amount")
        wallets = orm.select(Wallet,id=walletId,user_id=user_id)
        if len(wallets) == 0:
            return Response({'status': False, 'errors':"یافت نشد" }, status=status.HTTP_404_NOT_FOUND)

        if wallets[0].credit < int(amount) :
            return Response({'status': False, 'errors':"موجودی نا کافی" }, status=status.HTTP_404_NOT_FOUND)
        # try:
        orm.decharge(walletId,amount)
        orm.insert(Transaction, wallet_id=wallets[0].id,
                   paidAt=datetime.now().__str__(), amount=-1*amount)

        # except:
        #     return Response({'status': False, 'errors':"موجودی نا کافی" }, status=status.HTTP_404_NOT_FOUND)
        userWallets = orm.toDict(orm.select(Wallet, id=walletId))
        return Response(userWallets, status=status.HTTP_200_OK)

    def patch(self, request, format=None, *args, **kwargs):

        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors': "AUTHENTICATION ERROR"}, status=403)

        validator = FieldValidator(request.data)
        validator. \
            checkNotNone('name'). \
            checkNotNone('walletId'). \
            validate()
        if validator.statusCode != 200:
            return Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        name = request.data.get("name")
        id = request.data.get("walletId")
        if len(orm.select(Wallet,id=id,user_id=user_id)) == 0:
            return Response({"message": "کیف پول وجود ندارد."}, status.HTTP_400_BAD_REQUEST)
        orm.update(Wallet,id=id,name=name)
        userWallets = orm.toDict(orm.select(Wallet, id=id))
        return Response(userWallets, status=status.HTTP_200_OK)


class TransactionSearchController(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # try:

            try:
                user_id = request.GET['userId']
            except:
                return Response({'status': False, 'errors': "AUTHENTICATION ERROR"}, status=403)
            query = "SELECT * FROM \"API_transaction\"  WHERE ( 1=1"
            # query = 'SELECT "API_transaction"."id", "API_transaction"."reserve_id", "API_transaction"."wallet_id", "API_transaction"."paidAt", "API_transaction"."amount" FROM "API_transaction"'

            data = request.GET
            # x = Transaction.objects.filter(user_id=user_id)
            if data.get("min_amount",False):
                orm.checkForSqlInjection(data.get("min_amount"))
                query += " AND \"amount\" >= {}".format(float(data.get("min_amount")))
            if data.get("max_amount",False):
                orm.checkForSqlInjection(data.get("max_amount"))
                query += " AND \"amount\" <= {}".format(float(data.get("max_amount")))
            if data.get("to_date",False):
                orm.checkForSqlInjection(data.get("to_date"))
                query += " AND \"paidAt\" <= \'{}\'".format(stringToDate(data.get("to_date")).__str__())
            if data.get("from_date",False):
                orm.checkForSqlInjection(data.get("from_date"))
                query += " AND \"paidAt\" >= \'{}\'".format(stringToDate(data.get("from_date")).__str__())
            if data.get('walletId',False):
                orm.checkForSqlInjection(data.get("walletId"))
                query += " AND \"wallet_id\" =  {}".format(int(data.get('walletId')))
            query += ") ORDER BY \"paidAt\" DESC"
            if data.get("amount",False):
                query += ",\"amount\" DESC"
            res = orm.rawQuery(query)
            resDict = orm.toDict(res)
            return Response(resDict, status=status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)

def stringToDate(strDate):
    year, month, day = map(int, strDate.split("-"))

    return date(
        year=year,
        month=month,
        day=day
    )