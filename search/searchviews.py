from .models import Person
from package.models import Package
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from .filters import PersonFilter
from django.contrib.auth.decorators import login_required
def show_all_persons_page(request):
    context = {}

    filtered_persons = PersonFilter(
        request.GET,
        queryset = Package.objects.all()
    )


    context['filtered_persons'] = filtered_persons

    paginated_filtered_persons = Paginator(filtered_persons.qs, 2)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filtered_persons.get_page(page_number)

    context['person_page_obj'] = person_page_obj

    context['media_url'] = settings.MEDIA_URL

    return render(request, 'search.html', context=context)

@login_required
def profile_search_filter(request):
    context = {}

    filtered_persons = PersonFilter(
        request.GET,
        queryset = Package.objects.all()
    )


    context['filtered_persons'] = filtered_persons

    paginated_filtered_persons = Paginator(filtered_persons.qs, 2)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filtered_persons.get_page(page_number)

    context['person_page_obj'] = person_page_obj

    context['media_url'] = settings.MEDIA_URL

    return render(request, 'logged_search.html', context=context)