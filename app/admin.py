from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models import UserProfile, Tutor, Discipline, Review, Lesson


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


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'slug', 'experience_years', 'average_rating', 'created_at')
    list_filter = ('is_high_edu', 'experience_years', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'slug')
    filter_horizontal = ('favorites_by',)
    readonly_fields = ('created_at', 'average_rating')
    
    fieldsets = (
        ('Пользователь', {'fields': ('user', 'slug')}),
        ('Профессиональная информация', {
            'fields': ('age', 'experience_years', 'bio', 'is_high_edu')
        }),
        ('Информация системы', {
            'fields': ('created_at', 'favorites_by')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'ФИО'
    
    def average_rating(self, obj):
        rating = obj.average_rating
        return f'⭐ {rating}/5' if rating > 0 else 'Нет оценок'
    average_rating.short_description = 'Средняя оценка'


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor', 'price_per_hour', 'slug')
    list_filter = ('tutor', 'price_per_hour')
    search_fields = ('name', 'tutor__user__first_name', 'tutor__user__last_name')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Информация предмета', {
            'fields': ('name', 'slug', 'tutor', 'price_per_hour')
        }),
        ('Дополнительно', {
            'fields': ('description',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'tutor', 'grade', 'created_at')
    list_filter = ('tutor', 'grade', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'tutor__user__first_name', 'text')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Отзыв', {
            'fields': ('student', 'tutor', 'grade', 'text')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    get_student_name.short_description = 'Студент'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'tutor', 'discipline', 'scheduled_at', 'duration_minutes', 'total_price')
    list_filter = ('tutor', 'discipline', 'scheduled_at', 'duration_minutes')
    search_fields = ('student_name', 'student_email', 'tutor__user__first_name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'scheduled_at'
    
    fieldsets = (
        ('Студент', {
            'fields': ('student', 'student_name', 'student_email', 'student_phone')
        }),
        ('Урок', {
            'fields': ('tutor', 'discipline', 'scheduled_at', 'duration_minutes', 'total_price')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at')
        }),
    )