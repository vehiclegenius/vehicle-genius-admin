from django.contrib.auth.decorators import login_required
from django.urls import path

from summarytemplates import views

urlpatterns = [
    path('', login_required(views.current), name='current'),
    path('validate/', login_required(views.validate_and_preview_post), name='test-template'),
]
