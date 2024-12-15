from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('disease/', views.search_disease, name='disease'),
    
    path('patient/', views.search_patient, name='patient'),

    path('blog/', views.SearchBlogView.as_view(), name='q_blog'),
]
