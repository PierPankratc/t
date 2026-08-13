from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from app.models import Tutor, Discipline, Reviews, User


def tutors_list(request):
    
    q = request.GET.get('q', '').strip()
    tutors = Tutor.objects.all()
    if q:
        tutors = tutors.filter(name__icontains=q)
    tutors = tutors.prefetch_related('discipline_set')
    return render(request, 'tutors/list.html', {'tutors': tutors, 'q': q})


def tutor_detail(request, slug):
    
    tutor = get_object_or_404(Tutor, slug=slug)
    disciplines = Discipline.objects.filter(tutor=tutor)
    reviews = Reviews.objects.filter(tutor=tutor)

    discipline_names = disciplines.values_list('name', flat=True)
    recommendations = (
        Tutor.objects.filter(discipline__name__in=discipline_names)
        .exclude(pk=tutor.pk)
        .distinct()[:3]
    )

    return render(
        request,
        'tutors/detail.html',
        {
            'tutor': tutor,
            'disciplines': disciplines,
            'reviews': reviews,
            'recommendations': recommendations,
        },
    )

def favorite_list(request, slug, d_slug):

    tutor = get_object_or_404(Tutor, slug=slug)
    _discipline = get_object_or_404(Tutor.disciplines, slug=d_slug)

    return render(
        request,
        'favorite_list/html',
        {
            'tutor': tutor,
            'disciplines': _discipline
        }
    )


@require_http_methods(["POST"])
def toggle_favorite(request, tutor_slug):
    """Добавить или удалить преподавателя из избранного"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Для демо используем первого юзера, в реальном приложении используйте request.user
        tutor = get_object_or_404(Tutor, slug=tutor_slug)
        user = User.objects.first()
        
        if not user:
            logger.error(f'User not found for tutor {tutor_slug}')
            return JsonResponse({'error': 'User not found'}, status=400)
        
        if user in tutor.favorites_by.all():
            tutor.favorites_by.remove(user)
            is_favorite = False
            message = 'Удалено из избранного'
        else:
            tutor.favorites_by.add(user)
            is_favorite = True
            message = 'Добавлено в избранное'
        
        logger.info(f'Toggle favorite: user={user.id}, tutor={tutor_slug}, is_favorite={is_favorite}')
        
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'message': message
        })
    except Exception as e:
        logger.error(f'Error in toggle_favorite: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)


def favorite_tutors_list(request):
    """Список избранных преподавателей"""
    user = User.objects.first()  # Получите текущего пользователя
    
    if not user:
        return render(request, 'tutors/favorites.html', {'tutors': []})
    
    tutors = user.favorite_tutors.all().prefetch_related('discipline_set')
    return render(request, 'tutors/favorites.html', {'tutors': tutors})




