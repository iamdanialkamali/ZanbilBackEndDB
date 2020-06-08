import json


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from API.models import Sans, Service, ServiceFile, TimeTable,Business
import API.orm as orm
from API.ticketService import TicketManager
from ast import literal_eval

from API.validation import FieldValidator


class TicketController(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)
        validator = FieldValidator(request.POST)
        validator.checkNotNone('businessId'). \
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
        data = request.POST
        toUserId = data.get("toUserId",None)
        businessId = data.get("businessId")
        files = data.get("files",[])
        if isinstance(files,str):
            files = literal_eval(files)
        business = orm.select(Business,id=businessId)[0]
        admin = business.owner_id == user_id
        ticket = TicketManager.createTicket(request.POST.get("subject"),businessId,toUserId)
        ticket.save()
        if admin:
            TicketManager.addAdminMessage(ticket.id,data.get("text"),fromUserId=user_id,files=files)
        else:
            TicketManager.addUserMessage(ticket.id,data.get("text"),user_id,files)
        responseTicket = TicketManager.getTicket(ticket.id)
        return Response({
            'ticket': responseTicket
        }, status=status.HTTP_200_OK)

    # except Exception :
    #     return Response({},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, *args, **kwargs):
        validator = FieldValidator(request.GET)
        validator.checkNotNone('ticketId').\
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
        ticketId = request.GET['ticketId']
        responseTicket = TicketManager.getTicket(ticketId)
        return Response({
            'ticket': responseTicket
        }, status=status.HTTP_200_OK)




    def post(self, request, format=None, *args, **kwargs):

        try:
            user_id = request.GET['userId']
        except:
            return Response({'status': False, 'errors':"AUTHENTICATION ERROR"},status=403)

        validator = FieldValidator(request.POST)
        validator.checkNotNone('ticketId'). \
            checkNotNone('businessId'). \
            checkNotNone('text'). \
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)

        ticketId = request.POST.get('ticketId')
        data = request.POST
        files = data.get("files", [])
        if isinstance(files,str):
            files = literal_eval(files)
        businessId = data.get("businessId")
        business = orm.select(Business, id=businessId)[0]
        admin = business.owner_id == user_id
        if admin:
            TicketManager.addAdminMessage(ticketId, data.get("text"), fromUserId=user_id, files=files)
        else:
            TicketManager.addUserMessage(ticketId, data.get("text"), user_id, files)
        responseTicket = TicketManager.getTicket(ticketId)
        return Response({'ticket': responseTicket}, status=status.HTTP_200_OK)





class TicketSearchController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        validator = FieldValidator(request.GET)
        validator.checkNotNone('userId'). \
            checkNotNone('businessId'). \
            validate()
        if validator.statusCode != 200:
            Response({'status': False, 'errors': validator.getErrors()}, status=validator.statusCode)
        userId = request.GET.get('userId')
        businessId = request.GET.get('businessId')
        responseTicket = TicketManager.search(userId=userId,businessId=businessId)
        return Response({
            'ticket': responseTicket
        }, status=status.HTTP_200_OK)


