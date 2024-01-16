from django.urls import path
from . import views # . means the current folder 
urlpatterns = [
    path('sayhello',views.say_hello),
]
