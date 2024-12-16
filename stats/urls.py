from django.urls import path
from . import views

urlpatterns = [
    path('', views.StatsPageView.as_view(), name='stats_page'),
]
