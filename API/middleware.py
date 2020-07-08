import traceback
from django.core.exceptions import PermissionDenied, FieldError , ValidationError
from django.http import HttpResponse

from django.utils.deprecation import MiddlewareMixin

from rest_framework import status
import json
from rest_framework.response import Response
def jsonResponse(data={}, status=200):
    return HttpResponse(json.dumps(data),status=status, content_type='application/json')

class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
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
