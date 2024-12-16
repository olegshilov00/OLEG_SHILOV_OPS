from django.urls import path

from . import views

urlpatterns = [
    path("", views.MenuView.as_view(), name="index"),
    path("solve/", views.SolveView.as_view(), name="solve"),
    path("trainer/", views.TrainerView.as_view(), name="trainer"),
]
