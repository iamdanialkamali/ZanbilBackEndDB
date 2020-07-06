import jdatetime
import mongoengine_goodjson as gj
from mongoengine import *
import json
from datetime import datetime
from enum import Enum

class TicketEnum(Enum):
    DEPARTMENT_GATEWAY = 1
    DEPARTMENT_POS = 2
    DEPARTMENT_OTHER = 0
    DEPARTMENT_CLUB = 3

    STATUS_OPEN = 1
    STATUS_CLOSED = 0
    STATE_MESSAGE = 0

    NORMAL_MESSAGE = 1
    CLOSE_MESSAGE = 2
    OPEN_MESSAGE = 3
    ASSIGN_MESSAGE = 4
    FEEDBACK_MESSAGE = 4
    SEEN_MESSAGE = 5
    CRM_USER_ID = 3463#parisa
    CRM_PERMISSION = 101



def toJalaliDateTime(d, time = True):
    if d==None: return '-'
    if time == True:
        return jdatetime.datetime.fromgregorian(datetime=d).strftime("%Y/%m/%d-%H:%M:%S")
    else:
        return jdatetime.datetime.fromgregorian(datetime=d).strftime("%Y/%m/%d")


def toPrettyJalaliDateTime(dt):
    if dt is None: return '-'
    return jdatetime.datetime.fromgregorian(datetime=dt).aslocale('fa_IR').pretty()

class TicketMessage(gj.EmbeddedDocument):
    fromUserId = IntField()
    toUserId = IntField()
    text = StringField()
    type = IntField()
    createdAt = DateTimeField(required=True)
    readAt = DateTimeField()
    files = ListField(IntField(),)

    def read(self):
        self.readAt = datetime.now()


class Ticket(gj.Document):
    subject = StringField()
    status = IntField()
    userId = IntField()
    businessId = IntField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
    messages = EmbeddedDocumentListField(TicketMessage)

    meta = {
        'indexes': [
            {'fields': ['-userId']},
            {'fields': ['-businessId']},
            {'fields': ['-updatedAt']},
        ]
    }


    def addNormalMessage(self, text, fromUserId, fileIds=[], toUserId=None):
        self.messages.append(
            TicketMessage(
                text=text,
                fromUserId=fromUserId,
                toUserId=toUserId,
                createdAt=datetime.now(),
                files=fileIds
            )
        )
        self.updatedAt = datetime.now()
        self.save()
        return self



    def toDict(self, **options):
        dictedTicket = json.loads(self.to_json())
        if len(options) == 0:
            return dictedTicket
        wantedData = {}
        for key in options:
            wantedData[key] = dictedTicket[key]
        return wantedData


    def prettifyDates(self):
        ticket = self.toDict()
        ticket['createdAt'] = toJalaliDateTime(self.createdAt)
        # ticket['createdAtPretty'] = toPrettyJalaliDateTime(self.createdAt)
        ticket['updatedAt'] = toJalaliDateTime(self.updatedAt)
        # ticket['updatedAtPretty'] = toPrettyJalaliDateTime(self.updatedAt)

        for message_index in range(len(ticket['messages'])):
            # ticket['messages'][message_index]['createdAtPretty'] = toPrettyJalaliDateTime(
            #     self.messages[message_index].createdAt)
            ticket['messages'][message_index]['createdAt'] = toJalaliDateTime(self.messages[message_index].createdAt)
            if (self.messages[message_index].readAt):
                # ticket['messages'][message_index]['readAtPretty'] = toPrettyJalaliDateTime(
                #     self.messages[message_index].readAt)
                ticket['messages'][message_index]['readAt'] = toJalaliDateTime(self.messages[message_index].readAt)
        return ticket


    def filter_messages(self):
        self.messages = self.messages.filter(deletedAt=None).exclude(type=TicketEnum.SEEN_MESSAGE.value)

