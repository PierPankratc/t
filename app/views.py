from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.text import slugify
import logging

from app.models import Tutor, Discipline, Review, UserProfile, Lesson
from app.forms import StudentRegistrationForm, TutorRegistrationForm, CustomAuthenticationForm

logger = logging.getLogger(__name__)


def tutors_list(request):
    """List all tutors with filtering and search"""
    q = request.GET.get('q', '').strip()
    tutors = Tutor.objects.all()
    if q:
        tutors = tutors.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(bio__icontains=q)
        )
    tutors = tutors.prefetch_related('disciplines')
    return render(request, 'tutors/list.html', {'tutors': tutors, 'q': q})


def tutor_detail(request, slug):
    """Detailed view of a tutor profile"""
    tutor = get_object_or_404(Tutor, slug=slug)
    disciplines = Discipline.objects.filter(tutor=tutor)
    reviews = Review.objects.filter(tutor=tutor)

    discipline_names = disciplines.values_list('name', flat=True)
    recommendations = (
        Tutor.objects.filter(disciplines__name__in=discipline_names)
        .exclude(pk=tutor.pk)
        .distinct()[:3]
    )

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = request.user in tutor.favorites_by.all()

    return render(
        request,
        'tutors/detail.html',
        {
            'tutor': tutor,
            'disciplines': disciplines,
            'reviews': reviews,
            'recommendations': recommendations,
            'is_favorite': is_favorite,
        },
    )


@login_required(login_url='app:login')
@require_POST
def toggle_favorite(request, tutor_slug):
    """Add or remove tutor from favorites (AJAX)"""
    try:
        tutor = get_object_or_404(Tutor, slug=tutor_slug)
        user = request.user
        
        if user in tutor.favorites_by.all():
            tutor.favorites_by.remove(user)
            is_favorite = False
            message = 'Удалено из избранного'
        else:
            tutor.favorites_by.add(user)
            is_favorite = True
            message = 'Добавлено в избранное'
        
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'message': message
        })
    except Exception as e:
        logger.error(f'Error in toggle_favorite: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='app:login')
def favorite_tutors_list(request):
    """List of favorite tutors for logged-in user"""
    user = request.user
    tutors = user.favorite_tutors.all().prefetch_related('disciplines')
    return render(request, 'tutors/favorites.html', {'tutors': tutors})


# ============ AUTHENTICATION VIEWS ============


def register_student(request):
    """Register a new student"""
    if request.user.is_authenticated:
        return redirect('tutors:list')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}!')
            return redirect('app:tutors_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'auth/register_student.html', {'form': form})


def register_tutor(request):
    """Register a new tutor"""
    if request.user.is_authenticated:
        return redirect('tutors:list')
    
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, репетитор {user.first_name}!')
            return redirect('app:tutor_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TutorRegistrationForm()
    
    return render(request, 'auth/register_tutor.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('tutors:list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'app:tutors_list')
                return redirect(next_url)
        else:
            messages.error(request, 'Неверные учетные данные')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('app:tutors_list')


@login_required(login_url='app:login')
def user_dashboard(request):
    """User personal account (student)"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, 'Профиль пользователя не найден')
        return redirect('tutors:list')
    
    if profile.role != 'student':
        messages.error(request, 'Доступ только для студентов')
        return redirect('tutors:list')
    
    favorites = request.user.favorite_tutors.all()
    lessons = request.user.lessons.all().order_by('-scheduled_at')
    reviews = request.user.reviews_written.all().order_by('-created_at')
    
    return render(request, 'account/student_dashboard.html', {
        'profile': profile,
        'favorites': favorites,
        'lessons': lessons,
        'reviews': reviews,
    })


@login_required(login_url='app:login')
def tutor_dashboard(request):
    """Tutor personal account"""
    try:
        profile = request.user.profile
        tutor = request.user.tutor_profile
    except (UserProfile.DoesNotExist, Tutor.DoesNotExist):
        messages.error(request, 'Профиль репетитора не найден')
        return redirect('tutors:list')
    
    if profile.role != 'tutor':
        messages.error(request, 'Доступ только для репетиторов')
        return redirect('tutors:list')
    
    disciplines = tutor.disciplines.all()
    lessons = tutor.lessons.all().order_by('-scheduled_at')
    reviews = tutor.reviews.all().order_by('-created_at')
    favorite_count = tutor.favorites_by.count()
    
    return render(request, 'account/tutor_dashboard.html', {
        'profile': profile,
        'tutor': tutor,
        'disciplines': disciplines,
        'lessons': lessons,
        'reviews': reviews,
        'favorite_count': favorite_count,
    })





