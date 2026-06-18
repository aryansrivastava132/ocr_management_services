from django.urls import path
from . import views

urlpatterns = [
    path('',               views.index,          name='index'),
    path('api/scan/',      views.scan,            name='scan'),
    path('api/history/',   views.history_api,     name='history'),
    path('api/datechart/', views.date_chart_api,  name='date_chart'),
    path('api/report/',    views.download_report, name='report'),
]
