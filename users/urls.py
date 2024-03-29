from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.index_get), name='index'),
    path('<str:user>/<str:vehicle_id>', login_required(views.user_vehicle_get), name='user_vehicle'),
    path('<str:user>/<str:vehicle_id>/user_data', login_required(views.user_vehicle_user_data), name='user_vehicle_user_data'),
]
