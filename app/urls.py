from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    path('', views.tutors_list, name='list'),
    path('favorites/', views.favorite_tutors_list, name='favorites'),
    path('<slug:tutor_slug>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/', views.tutor_detail, name='detail'),
]
