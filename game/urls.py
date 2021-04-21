from django.urls import path
from . import views


app_name = 'game'
template_dir = 'game/'

urlpatterns = [
    path('add/',
         views.GameCreate.as_view(template_name=template_dir + 'add.html'),
         name='add'),
    path('schedule/',
         views.GameSchedule.as_view(template_name=template_dir + 'schedule.html'),
         name='schedule'),
]
