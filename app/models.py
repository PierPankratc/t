from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.IntegerField(unique=True)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='photos', blank=True)
    is_blocked  = models.BooleanField(db_default=False)

    class Meta:
            verbose_name = "Студент"           
            verbose_name_plural = "Студенты" 
   

class Tutor(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.IntegerField(unique=True)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='photos', blank=True)
    is_blocked  = models.BooleanField(db_default=False)
    is_high_edu = models.BooleanField(db_default=False)
    age = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Репетитор"           
        verbose_name_plural = "Репетиторы" 


class Discipline(models.Model):
     tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
     name = models.CharField(max_length=20)
     price = models.DecimalField(decimal_places=2, max_digits=7, validators=[MinValueValidator(0)])
     durations = models.IntegerField(validators=[MinValueValidator(0)])

     class Meta:
        verbose_name = "Предмет"           
        verbose_name_plural = "Предметы"


class Reviews(models.Model):
      tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
      discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
      grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
      review = models.TextField(max_length=250, blank=True)

      class Meta:
        verbose_name = "Отзыв"           
        verbose_name_plural = "Отзывы"








