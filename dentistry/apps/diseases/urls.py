from django.urls import path
from . import views

app_name = 'diseases'
urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    
    path('part_blog/<int:id>/', views.part_blog, name='part_blog'),

    path('detail_blog/<int:id>/', views.DetailBlogView.as_view(), name='detail_blog'),

    path('selected/', views.ResultDescriptionView.as_view(), name='selected'),
]
