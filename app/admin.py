from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models import UserProfile, Tutor, Discipline, Review


# Extend the default User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('role', 'phone_number', 'avatar', 'is_blocked')


class ExtendedUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin with extended admin
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'is_blocked')
    list_filter = ('role', 'is_blocked')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_editable = ('is_blocked',)

from django.contrib import admin
from .models import Tutor

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    # Используем название метода (без скобок)
    list_display = ('user', 'slug', 'experience_years', 'created_at')
    
    # Убираем average_rating из list_filter (это не поле БД)
    list_filter = ('is_high_edu', 'experience_years', 'created_at')
    
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'slug')
    filter_horizontal = ('favorites_by',)
    
#     # Убираем average_rating из readonly_fields (это не поле БД)
#     readonly_fields = ('created_at',)
    
#     fieldsets = (
#         ('Пользователь', {'fields': ('user', 'slug')}),
#         ('Профессиональная информация', {
#             'fields': ('age', 'experience_years', 'about', 'is_high_edu')
#         }),
#         ('Информация системы', {
#             'fields': ('created_at', 'favorites_by')
#         }),
#     )
    
#     def get_full_name(self, obj):
#         return obj.user.get_full_name() or obj.user.username
#     get_full_name.short_description = 'ФИО'
    
    # def get_average_rating(self, obj):
    #     """Отображает рейтинг в админке"""
    #     rating = obj.average_rating  # Используем @property из модели
    #     if rating > 0:
    #         return f'⭐ {rating:.2f}/5'
#     #     return 'Нет оценок'
#     # get_average_rating.short_description = 'Средняя оценка'

# @admin.register(Discipline)
# class DisciplineAdmin(admin.ModelAdmin):
#     list_display = ('name', 'tutor', 'price_per_hour', 'slug')
#     list_filter = ('tutor', 'price_per_hour')
#     search_fields = ('name', 'tutor__user__first_name', 'tutor__user__last_name')
#     prepopulated_fields = {'slug': ('name',)}
    
#     fieldsets = (
#         ('Информация предмета', {
#             'fields': ('name', 'slug', 'tutor', 'price_per_hour')
#         }),
#         ('Дополнительно', {
#             'fields': ('description',)
#         }),
#     )


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('get_student_name', 'tutor', 'grade', 'created_at')
#     list_filter = ('tutor', 'grade', 'created_at')
#     search_fields = ('student__first_name', 'student__last_name', 'tutor__user__first_name', 'text')
#     readonly_fields = ('created_at', 'updated_at')
    
#     fieldsets = (
#         ('Отзыв', {
#             'fields': ('student', 'tutor', 'grade', 'text')
#         }),
#         ('Метаданные', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_student_name(self, obj):
#         return obj.student.get_full_name() or obj.student.username
#     get_student_name.short_description = 'Студент'

