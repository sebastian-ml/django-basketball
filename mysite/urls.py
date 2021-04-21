from django.urls import path
from . import views

app_name = 'home'
template_dir = 'mysite/'

urlpatterns = [
    path('',
         views.Home.as_view(template_name=template_dir + 'home.html'),
         name='home')
]
