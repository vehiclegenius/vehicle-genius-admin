from django.contrib.auth.decorators import login_required
from django.urls import path

from promptfeedbacks import views

urlpatterns = [
    path('', login_required(views.index_get), name='index'),
    path('<str:pk>/resolve', login_required(views.resolve_post), name='resolve'),
]
