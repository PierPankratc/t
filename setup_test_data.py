#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutors.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import UserProfile, Tutor, Discipline

# Create a test student user
student_user = User.objects.create_user(
    username='student@example.com',
    email='student@example.com',
    password='password123',
    first_name='Ivan',
    last_name='Petrov'
)
print(f"✓ Created student: {student_user.username}")

# Create a test tutor user
tutor_user = User.objects.create_user(
    username='tutor@example.com',
    email='tutor@example.com',
    password='password123',
    first_name='Maria',
    last_name='Sokolova'
)
print(f"✓ Created tutor user: {tutor_user.username}")

# Update tutor profile role
tutor_profile = tutor_user.profile
tutor_profile.role = 'tutor'
tutor_profile.phone_number = '+79991234567'
tutor_profile.save()
print(f"✓ Updated tutor profile role: {tutor_profile.role}")

# Create Tutor profile
tutor = Tutor.objects.create(
    user=tutor_user,
    slug='maria-sokolova',
    experience_years=5,
    bio='Опытный репетитор по математике и физике',
    is_high_edu=True,
    age=32
)
print(f"✓ Created tutor: {tutor.user.get_full_name()}")

# Create disciplines for the tutor
discipline1 = Discipline.objects.create(
    tutor=tutor,
    name='Математика',
    slug='matematika',
    price_per_hour=600,
    description='Помощь в учебе по математике для школьников и студентов'
)
print(f"✓ Created discipline: {discipline1.name}")

discipline2 = Discipline.objects.create(
    tutor=tutor,
    name='Физика',
    slug='fizika',
    price_per_hour=700,
    description='Подготовка к ЕГЭ по физике'
)
print(f"✓ Created discipline: {discipline2.name}")

print("\n✅ Test data created successfully!")
print(f"   Student: {student_user.get_full_name()} ({student_user.email}, пароль: password123)")
print(f"   Tutor: {tutor.user.get_full_name()} ({tutor_user.email}, пароль: password123)")
print(f"   Admin: admin (пароль: admin123)")
print("\n🌐 Access points:")
print("   - Home/Tutors list: http://127.0.0.1:8000/tutors/")
print("   - Login: http://127.0.0.1:8000/auth/login/")
print("   - Student registration: http://127.0.0.1:8000/auth/register/student/")
print("   - Tutor registration: http://127.0.0.1:8000/auth/register/tutor/")
print("   - Admin panel: http://127.0.0.1:8000/admin/")
