import json

from bson import ObjectId
from mongoengine.queryset.visitor import Q
from API.models import  User,MessageFile
from API.mongoModel import Ticket,TicketEnum
from datetime import datetime
import API.orm as orm
class TicketManager:

    @staticmethod
    def createTicket(subject, businessId, userId):

        newTicket = Ticket(
            subject=subject,
            businessId=businessId,
            userId=userId,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        newTicket.save()

        return newTicket


    @staticmethod
    def addMessageAndFiles(ticket, text, fromUserId, toUserId=None, files=[]):
        ticket.addNormalMessage(text, fromUserId, files, toUserId)
        return ticket

    # @staticmethod
    # def addAdminMessage(ticketId, text, fromUserId, files=[]):
    #     ticket = Ticket.objects.get(id=ObjectId(ticketId))
    #     toUserId = ticket.userId
    #     ticket = TicketManager.addMessageAndFiles(ticket, text=text, fromUserId=fromUserId, toUserId=toUserId,
    #                                               files=files)
    #     return ticket.toDict()

    @staticmethod
    def addUserMessage(ticketId, text, fromUserId, files=[]):
        filters = {'id': ObjectId(ticketId) if isinstance(ticketId,str) else ticketId}
        if fromUserId is not None:
            filters['userId'] = fromUserId
        ticket = Ticket.objects.get(**filters)
        ticket = TicketManager.addMessageAndFiles(ticket, text=text, fromUserId=fromUserId,  files=files)
        ticket.save()
        return ticket

    @staticmethod
    def openTicket(ticketId, fromUserId, admin=False):
        filters = {'id': ObjectId(ticketId) if isinstance(ticketId,str) else ticketId}
        if admin is False:
            filters['userId'] = fromUserId
        ticket = Ticket.objects.get(**filters)
        if ticket is None or ticket.status == TicketEnum.STATUS_OPEN.value:
            return None
        ticket.status = TicketEnum.STATUS_OPEN.value
        result = ticket.addLogMessage(text="OPENED",fromUserId=fromUserId, type=TicketEnum.OPEN_MESSAGE.value, toUserId=ticket.userId, readAt=datetime.now())
        ticket.save()
        dictedTickets = ticket.prettifyDates()
        dictedTickets = TicketManager.addNameOfUserToMessages(dictedTickets)
        return dictedTickets

    @staticmethod
    def closeTicket(ticketId, fromUserId, toUserId=None, admin=False):
        filters = {'id': ObjectId(ticketId)}
        if admin is False:
            filters['userId'] = fromUserId
        ticket = Ticket.objects.get(**filters)

        if ticket is None or ticket.status == TicketEnum.STATUS_CLOSED.value:
            return None
        ticket.status = TicketEnum.STATUS_CLOSED.value
        result = ticket.addLogMessage(text="CLOSED", fromUserId=fromUserId, type=TicketEnum.CLOSE_MESSAGE.value,toUserId=ticket.userId, readAt=datetime.now())
        ticket.save()
        dictedTickets = ticket.prettifyDates()
        dictedTickets = TicketManager.addNameOfUserToMessages(dictedTickets)
        return dictedTickets

    @staticmethod
    def search(userId=None,  businessId=None):
        filters = {}
        if userId:
            filters['userId'] = userId
            if businessId:
                filters['businessId'] = businessId

        total = Ticket.objects.filter(**filters).count()
        tickets = Ticket.objects.filter(**filters).order_by('-updatedAt')


        return {'data': json.loads(tickets.to_json()), 'total': total}

    @staticmethod
    def getTicket(ticketId, userId=None,admin=False):
        if not isinstance(ticketId,ObjectId):
            filters = {'id': ObjectId(ticketId)}
        else:
            filters = {'id': ticketId}

        # if not admin:
        #     filters['userId'] = userId

        ticket = Ticket.objects.get(**filters)
        dictedTicket = ticket.prettifyDates()
        dictedTicket = TicketManager.addNameOfUserToMessages(dictedTicket)

        return dictedTicket


    @staticmethod
    def addNameOfUserToMessages(dictedTickets):
        idToName = {0: 'سیستم'}
        messages = dictedTickets['messages']
        for index, message in enumerate(messages):
            id = message['fromUserId']
            if idToName.get(id, None) is None:
                userName = orm.select(User,id=id)
                if len(userName) == 0:
                    userName = orm.select(User,id=1)
                else:
                    userName = userName[0].username
                    print("IDDDDDDDDDDD   ",id)
                idToName[id] = userName

            message['name'] = idToName[id]
            message['attachments'] = [orm.toDict(orm.select(MessageFile,id=x)) for x in message['files']]
            dictedTickets['messages'][index] = message

        return dictedTickets

