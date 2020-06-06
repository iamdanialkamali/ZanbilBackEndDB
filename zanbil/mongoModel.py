from bson import ObjectId
from mongoengine import *
import mongoengine_goodjson as gj
from datetime import datetime, timedelta
import json


class TicketMessage(gj.EmbeddedDocument):
    fromUserId = IntField()
    toUserId = IntField()
    text = StringField()
    type = IntField()
    createdAt = DateTimeField(required=True)
    readAt = DateTimeField()
    deletedAt = DateTimeField()
    files = ListField(IntField(),)
    fromDepartment = IntField()
    toDepartment = IntField()
    label = IntField()
    score = IntField()
    feedback = StringField()
    deletedAt = DateTimeField()

    def read(self):
        self.readAt = datetime.now()


class Ticket(gj.Document):
    subject = StringField()
    department = IntField()
    departments = ListField(IntField(), default=[TicketEnum.CRM_PERMISSION.value])
    assignees = ListField(IntField(), default=[TicketEnum.CRM_USER_ID.value])
    assignee = IntField(default=TicketEnum.CRM_USER_ID.value)
    labels = ListField(IntField())
    status = IntField()
    userId = IntField()
    waiting = BooleanField(default=False)
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
    score = IntField()
    feedback = StringField()
    hasAdminRead = BooleanField(default=True)
    hasUserRead = BooleanField(default=True)
    messages = EmbeddedDocumentListField(TicketMessage)

    meta = {
        'indexes': [
            {'fields': ['-userId']},
            {'fields': ['-updatedAt']},
        ]
    }

    def setFeedbackAndScore(self, user, score, feedback):
        if self.score is None:
            self.addLogMessage(text="FEEDBACK", fromUserId=user.id,feedback=feedback, type=TicketEnum.FEEDBACK_MESSAGE.value, score=score,readAt=datetime.now())
            self.update(score=score, feedback=feedback)
            return True
        else:
            return False

    def isClosed(self):
        return self.status == TicketEnum.STATUS_CLOSED.value

    def readMessages(self, userId, admin):
        if admin:
            self.hasAdminRead = True
        else:
            self.hasUserRead = True
        for message in self.messages.filter(readAt=None, toUserId=userId):
            # if message.readAt is None and (message.toUserId == userId ) and admin == False:
            #     message.read()
            message.read()
        self.save()

    def addNormalMessage(self, text, fromUserId, fileIds=[], toUserId=None):
        self.messages.append(
            TicketMessage(
                text=text,
                type=TicketEnum.NORMAL_MESSAGE.value,
                fromUserId=fromUserId,
                toUserId=toUserId,
                createdAt=datetime.now(),
                files=fileIds
            )
        )
        if toUserId is None:
            self.hasAdminRead = False
        else:
            self.hasUserRead = False
        self.updatedAt = datetime.now()
        self.save()

        return self

    def addLogMessage(self,*args,**kwargs):
        self.messages.append(
            TicketMessage(**kwargs,createdAt=datetime.now())
        )
        self.save()
        return self

    def addSeenMessage(self, reqUser):
        self.addLogMessage(
            text='SEEN', fromUserId=reqUser, type=TicketEnum.SEEN_MESSAGE.value, readAt=datetime.now()
        )
        self.save()
        return True

    def toDict(self, **options):
        dictedTicket = json.loads(self.to_json())
        if len(options) == 0:
            return dictedTicket
        wantedData = {}
        for key in options:
            wantedData[key] = dictedTicket[key]
        return wantedData

    @classmethod
    def getUserUnreadTicketsCount(cls, userId,admin):
        if admin:
            return cls.objects(hasAdminRead=False).count()
        else:
            return cls.objects(userId=userId, hasUserRead=False).count()

    def getUnreadMessagesCount(self, userId,admin):
        if admin:
            return int(not self.hasAdminRead)
        return self.messages.filter(deletedAt=None,readAt=None, toUserId=userId,
                                    type=1).count() if self.status != TicketEnum.STATUS_CLOSED else 0

    def prettifyDates(self):
        ticket = self.toDict()
        ticket['createdAt'] = toJalaliDateTime(self.createdAt)
        ticket['createdAtPretty'] = toPrettyJalaliDateTime(self.createdAt)
        ticket['updatedAt'] = toJalaliDateTime(self.updatedAt)
        ticket['updatedAtPretty'] = toPrettyJalaliDateTime(self.updatedAt)

        for message_index in range(len(ticket['messages'])):
            ticket['messages'][message_index]['createdAtPretty'] = toPrettyJalaliDateTime(
                self.messages[message_index].createdAt)
            ticket['messages'][message_index]['createdAt'] = toJalaliDateTime(self.messages[message_index].createdAt)
            if (self.messages[message_index].readAt):
                ticket['messages'][message_index]['readAtPretty'] = toPrettyJalaliDateTime(
                    self.messages[message_index].readAt)
                ticket['messages'][message_index]['readAt'] = toJalaliDateTime(self.messages[message_index].readAt)
        return ticket

   # def isUnreadForAssignee(self):
    #     if self.messages[0].readAt is None and self.messages[0].type ==  TicketEnum.ASSIGN_MESSAGE.value :
    #         return True
    #     return False

    def assign(self, fromUserId, departmentId, assignee, label=-1, addLog=True):
        if addLog:
            self.addLogMessage(text="ASSIGNED", fromUserId=fromUserId,type=TicketEnum.ASSIGN_MESSAGE.value, toUserId=assignee,
                               label=label, fromDepartment=self.department, toDepartment=departmentId)
        self.department = departmentId
        self.departments.append(departmentId)
        if fromUserId != self.assignee:
            self.assignees.append(fromUserId)
        self.assignees.append(assignee)
        self.assignee = assignee
        self.labels.append(label)
        self.hasAdminRead = False
        self.save()

    def setWaiting(self, flag):
        self.update(waiting=flag)
        return self.toDict()

    def filter_messages(self):
        self.messages = self.messages.filter(deletedAt=None).exclude(type=TicketEnum.SEEN_MESSAGE.value)


    # def hasUnreadMessage(self):
    #     if len(self.messages.filter(type=1)) == 0:
    #         return 0
    #     if self.messages.filter(type=1)[-1].toUserId == None and self.status != TicketEnum.STATUS_CLOSED.value and self.messages.filter()[-1].type != TicketEnum.OPEN_MESSAGE.value :
    #         return 1
    #     return 0

