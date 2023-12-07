from django.urls import path
from . import views

app_name = "dict"

urlpatterns = [
    path("", views.lookup, name='lookup')
]