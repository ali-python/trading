from .views import IndexView
from django.urls import path

urlpatterns = [
    path('index/', IndexView.as_view(), name='index')


]