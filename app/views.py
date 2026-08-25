
from django.shortcuts import render

from app.models import Tutor


def tutor_list(request):
    tutors = Tutor.objects.filter(is_blocked = False).all()
    sort = request.GET.get('sort')
    match sort:
        # case 'last': tutors =  tutors.order_by('created_at')
        case 'high_edu': tutors = tutors.filter(is_high_edu = True)
        case 'rating': tutors = tutors.order_by('average_rating')
        # case None: tutors = tutors.order_by('average_rating')

    return render(request, 'tutors/list.html', context={'tutors': tutors})