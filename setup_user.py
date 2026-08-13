import os
import sys
import django

# Добавить путь к проекту
sys.path.insert(0, r'c:\Users\user\Desktop\t')

# Установить переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutors.settings')

# Инициализировать Django
django.setup()

from app.models import User

# Проверим, есть ли уже пользователи
existing_users = User.objects.all()
if existing_users.exists():
    print(f"✓ В базе данных уже есть {existing_users.count()} пользователей:")
    for user in existing_users:
        print(f"  - {user.name} ({user.email})")
else:
    print("Создаю тестового пользователя...")
    user = User.objects.create(
        name="Иван Петров",
        email="ivan@test.com",
        phone_number=79991234567,
        password="test123"
    )
    print(f"✓ Пользователь создан: {user.name} ({user.email})")
