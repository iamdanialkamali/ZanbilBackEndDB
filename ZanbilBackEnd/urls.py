"""ZanbilBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
urlpatterns = []
# import zanbil.frontend.user as user
# import zanbil.frontend.business as business
# import zanbil.views as view
#
#
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#     path('v1/business/', business.BusinessAPI.as_view()),
#     path('v1/user/', user.UserAPI.as_view()),
#     path('user/', view.UserAPI.as_view()),
#     path('business/', view.BusinessAPI.as_view()),
#     path('category/', view.CategoryAPI.as_view()),
#     path('file/', view.FileAPI.as_view()),
#     path('reserve/', view.ReserveAPI.as_view()),
#     path('review/', view.ReviewAPI.as_view()),
#     path('service/', view.ServiceAPI.as_view()),
#     path('transaction/', view.TransactionAPI.as_view()),
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

from API.Business import BusinessController
from API.Service import ServiceController,SearchController
from API.Category import CategoryController
from API.Review import ReviewController
from API.AccountPage import AccountPageController
from API.Reserve import ReserveController
from API.Uploader import Image
from API.Dashboard import DashboardController
from API.Cancellation import CancellationController
from API.Ticket import TicketController,TicketSearchController
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/business/',BusinessController.as_view()),
    path('api/service/', ServiceController.as_view()),
    path('api/service/search/',SearchController.as_view()),
    path('api/category/', CategoryController.as_view()),
    path('api/service/review/',ReviewController.as_view()),
    path('api/user/',AccountPageController.as_view()),
    path('api/dashboard/',DashboardController.as_view()),
    path('api/service/reserve/',ReserveController.as_view()),
    path('api/file/',Image.as_view()),
    path('api/cancellation/',CancellationController.as_view()),
    path('api/ticket/',TicketController.as_view()),
    path('api/ticket/search/',TicketSearchController.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
