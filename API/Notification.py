from kavenegar import *

from django.core.mail import send_mail
from .models import User,Sans
import API.orm as orm
class NotificationController:

    @staticmethod
    def Notify(user_id, sans_id, date):
        user = orm.select(User,id=user_id)[0]
        sans = orm.select(Sans,id=sans_id)[0]
        message = "Resreve Has been set on\n " + date + "\n " +sans.startTime +" to  " +sans.endTime + "\n for business "+sans.timetable.business.name +" \n at address  " +sans.timetable.business.address

        NotificationController.sendEmail(user.email,message)
        NotificationController.sendEmail(sans.timetable.business.email,message)
        NotificationController.sendMessage(user.phone_number,message)
        return 1

    @staticmethod
    def sendEmail(email ,message):
        try:
            send_mail('Notification', message, 'notif@sandboxeb808a33cc074adb9fb924eef69c024a.mailgun.org',
                      ['daniel.kamali@yahoo.com', email])
            return 1
        except Exception:
            return 0
    @staticmethod
    def sendMessage(number, message):
        api = KavenegarAPI('434D634935754F355537366E526570396666524B41584A61752F426F79415944')
        params = {
            'sender': '100065995',
            'receptor': number,
            'message': message
        }
        try:
            api.sms_send(params)
            return 1
        except Exception:
            return 0



