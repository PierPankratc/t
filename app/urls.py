from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    path('', views.tutors_list, name='list'),
    path('<slug:slug>/', views.tutor_detail, name='detail'),
]
