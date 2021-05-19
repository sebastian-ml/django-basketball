from django.urls import path
from . import views


app_name = 'gamestats'
template_dir = 'gamestats/'

urlpatterns = [
    path('ranking/',
         views.GameStatsList.as_view(template_name=template_dir + 'ranking.html'),
         name='ranking'),
    path('schedule/',
         views.GameSchedule.as_view(template_name=template_dir + 'schedule.html'),
         name='schedule'),
]
