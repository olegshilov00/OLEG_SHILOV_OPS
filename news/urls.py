from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('category/<slug:slug>/', views.NewsByCategoryView.as_view(), name='news_by_category'),
    path('tag/<slug:slug>/', views.NewsByTagView.as_view(), name='news_by_tag'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]
