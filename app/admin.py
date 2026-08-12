from django.contrib import admin

from app.models import Discipline, Reviews, Tutor, User

# Register your models here.
@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'age', 'is_blocked', 'is_high_edu']
    list_filter = ['name', 'email', 'is_high_edu','is_blocked']
    search_fields = ['name', 'email']
    prepopulated_fields = {'slug': ('name',)}
    # ordering = ['-rating']
    # readonly_fields = ['id']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'durations', 'price', 'tutor']
    list_filter = ['name', 'durations', 'price', 'tutor']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'tutor', 'discipline', 'grade']
    list_filter = ['tutor', 'discipline', 'grade']
    search_fields = ['tutor_id', 'discipline_id', 'review']
    autocomplete_fields = ['tutor', 'discipline']
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_filter = ['id', 'name']
    search_fields = ['name']
    # autocomplete_fields = ['tutor', 'discipline']