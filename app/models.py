from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extended user profile to handle roles"""
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('tutor', 'Репетитор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='', verbose_name='Пользователь')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='Роль')
    avatar = models.ImageField(upload_to='photos', blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Tutor(models.Model):
    """Tutor profile with teaching information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile', verbose_name='Пользователь')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    is_high_edu = models.BooleanField(default=False, verbose_name='Есть высшее образование')
    age = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Возраст')
    experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Лет опыта')
    bio = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    favorites_by = models.ManyToManyField(User, related_name='favorite_tutors', blank=True, verbose_name='В избранном у')
    
    class Meta:
        verbose_name = "Репетитор"
        verbose_name_plural = "Репетиторы"
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.grade for r in reviews) / reviews.count(), 1)
        return 0
           


class Discipline(models.Model):
    """Subject/Discipline taught by tutors"""
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='disciplines', verbose_name='Преподаватель')
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=7, validators=[MinValueValidator(0)], default=500, verbose_name='Цена за час')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        unique_together = ('tutor', 'slug')
    
    def __str__(self):
        return f"{self.name} ({self.tutor})"


class Review(models.Model):
    """Student reviews for tutors"""
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='reviews', verbose_name='Репетитор')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written', verbose_name='Студент')
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    text = models.TextField(blank=True, verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('tutor', 'student')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student} -> {self.tutor}: {self.grade}/5"


class Lesson(models.Model):
    """Booked lessons"""
    DURATION_CHOICES = [(30, '30 мин'), (60, '60 мин'), (90, '90 мин'), (120, '120 мин')]
    
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='lessons', verbose_name='Репетитор')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', verbose_name='Студент')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Предмет')
    student_name = models.CharField(max_length=100, verbose_name='Имя студента')
    student_email = models.EmailField(verbose_name='Email студента')
    student_phone = models.CharField(max_length=20, verbose_name='Телефон студента')
    scheduled_at = models.DateTimeField(verbose_name='Дата и время урока')
    duration_minutes = models.IntegerField(choices=DURATION_CHOICES, verbose_name='Длительность (мин)')
    total_price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Итоговая стоимость')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"{self.student_name} -> {self.tutor} ({self.scheduled_at})"








