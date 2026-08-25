from datetime import datetime
from django.contrib import admin
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extended user profile to handle roles"""
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('tutor', 'Репетитор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Профиль', verbose_name='Пользователь')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='Роль')
    avatar = models.ImageField(upload_to='photos', blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
            if not self.slug:
                base_slug = slugify(self.user.username)
                slug = base_slug
                counter = 1
                while Tutor.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
            super().save(*args, **kwargs)


class Tutor(models.Model):
    """Tutor profile with teaching information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile', verbose_name='Пользователь')
    slug = models.SlugField(unique=True)
    is_high_edu = models.BooleanField(default=False, verbose_name='Высшее образование')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    age = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Возраст')
    experience_years = models.DecimalField(default=0, decimal_places=1, max_digits=6, validators=[MinValueValidator(0)], verbose_name='Лет опыта')
    experience_years = models.DecimalField(default=0, decimal_places=1, max_digits=6, validators=[MinValueValidator(0)], verbose_name='Лет опыта')
    about = models.TextField(blank=True, verbose_name='Описание')
    favorites_by = models.ManyToManyField(User, related_name='favorite_tutors', blank=True, verbose_name='В избранном у')
    created_at = models.DateTimeField(auto_now_add=True)

    
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

    @admin.display(description='Средний рейтинг')
    def admin_average_rating(self):
        return self.average_rating

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            while Tutor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Discipline(models.Model):
    """Subject/Discipline taught by tutors"""
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='disciplines', verbose_name='Преподаватель')
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=7, validators=[MinValueValidator(0)], default=1000, verbose_name='Цена за час')
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


class Messagers(models.Model):

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='messagers', verbose_name='Месседжеры')
    name = models.CharField(max_length=20)
    link = models.CharField(unique=True)




