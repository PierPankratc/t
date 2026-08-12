from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from app.models import Tutor, Discipline, Reviews


def tutors_list(request):
    """List view with simple name search by GET parameter `q`.

    Example: /tutors/?q=ivan
    """
    q = request.GET.get('q', '').strip()
    tutors = Tutor.objects.all()
    if q:
        tutors = tutors.filter(name__icontains=q)
    tutors = tutors.prefetch_related('discipline_set')
    return render(request, 'tutors/list.html', {'tutors': tutors, 'q': q})


def tutor_detail(request, slug):
    """Detail view for a tutor and recommendations.

    Recommendations: up to 3 other tutors who teach any of the same disciplines.
    """
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

