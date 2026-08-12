from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя')
    # surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.IntegerField(unique=True, verbose_name='телефон')
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='photos', blank=True)
    is_blocked  = models.BooleanField(default=False, verbose_name='заблокирован')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
            verbose_name = "Студент"           
            verbose_name_plural = "Студенты" 

    def __str__(self):
         return self.name
   

class Tutor(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя')
    slug = models.SlugField(primary_key=True)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.IntegerField(unique=True, verbose_name='телефон')
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='photos', blank=True, default='photos/OIP-2342034818.jpg')
    is_blocked  = models.BooleanField(default=False, verbose_name='заблокирован')
    is_high_edu = models.BooleanField(default=False, verbose_name='Есть высшее обр.')
    age = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Возраст')
    description = models.TextField(max_length=250, blank=True, verbose_name='Подробнее')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')


    class Meta:
        verbose_name = "Репетитор"           
        verbose_name_plural = "Репетиторы" 

    def __str__(self):
        return self.name
           


class Discipline(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name='Преподаватель')
    name = models.CharField(max_length=20, verbose_name='название')
    slug = models.SlugField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, validators=[MinValueValidator(0)], verbose_name='цена')
    durations = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='длительность')

    class Meta:
        verbose_name = "Предмет"           
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name
       


class Reviews(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name='Преподаватель')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Предмет')
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, verbose_name='Оценка')
    review = models.TextField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Отзыв"           
        verbose_name_plural = "Отзывы"

    def __str__(self):
         return f'{self.tutor} - {self.discipline}: {self.grade}''/''5'

    








