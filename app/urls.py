from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Tutor browsing URLs
    path('tutors/', views.tutors_list, name='tutors_list'),
    path('tutors/favorites/', views.favorite_tutors_list, name='favorites'),
    path('tutors/<slug:tutor_slug>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('tutors/<slug:slug>/', views.tutor_detail, name='tutor_detail'),
    
    # Authentication URLs
    path('auth/register/student/', views.register_student, name='register_student'),
    path('auth/register/tutor/', views.register_tutor, name='register_tutor'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # Account/Dashboard URLs
    path('account/dashboard/student/', views.user_dashboard, name='student_dashboard'),
    path('account/dashboard/tutor/', views.tutor_dashboard, name='tutor_dashboard'),
]
