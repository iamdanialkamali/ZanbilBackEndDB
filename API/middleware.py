import traceback
from datetime import datetime

from django.core.exceptions import PermissionDenied, FieldError , ValidationError
from django.http import HttpResponse

from django.utils.deprecation import MiddlewareMixin

from rest_framework import status
import json
from rest_framework.response import Response

from API import orm
from API.models import ActivityLog


def jsonResponse(data={}, status=200):
    return HttpResponse(json.dumps(data),status=status, content_type='application/json')
def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        payload = request.POST.copy()
        for k in ['password', 'pass']:
            payload.pop(k, None)

        if isinstance(exception, PermissionDenied):
            return jsonResponse({'message': exception.__str__() or 'شما اجازه دسترسی به این قسمت را ندارید!', 'success': False}, status.HTTP_400_BAD_REQUEST)
        if isinstance(exception, ValidationError):
            return jsonResponse(
                {'message': exception.__str__() or 'شما اجازه دسترسی به این قسمت را ندارید!', 'success': False}, status.HTTP_400_BAD_REQUEST)

        # print(traceback.format_exc())
        return jsonResponse(
            {'message': 'خطای داخلی سرور، زیبال این خطا را بررسی و برطرف خواهد کرد', 'status': False, 'result': -1,"begaie":
             traceback.format_exc()},
            status.HTTP_400_BAD_REQUEST)
    # One-time configuration and initialization.

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        data = request.body.decode()
        response = get_response(request)
        if len(response.content)<4000:
            orm.safeInsert(
                ActivityLog,
                ip=getClientIp(request),
                url=request.build_absolute_uri(),
                request=data,
                createdAt=datetime.now().__str__(),
                response=response.content.decode()
            )

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware