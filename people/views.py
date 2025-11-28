from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Person
from .forms import PersonRegistrationForm, PersonAdminForm

# Create your views here.

def register(request):
    """Public registration form - no login required."""
    if request.method == 'POST':
        form = PersonRegistrationForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(request, f'Thank you {person.first_name}! You have been registered successfully.')
            return redirect('people:register_success')
    else:
        form = PersonRegistrationForm()
    
    return render(request, 'people/register.html', {'form': form})


def register_success(request):
    """Success page after registration."""
    return render(request, 'people/register_success.html')


@login_required
def person_list(request):
    """List all registered people (admin only)."""
    search_query = request.GET.get('search', '')
    people = Person.objects.all()
    
    if search_query:
        people = people.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Pagination: 25 people per page
    paginator = Paginator(people, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'people': page_obj,  # for backward compatibility in template
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'people/person_list.html', context)


@login_required
def person_detail(request, pk):
    """View details of a specific person (admin only)."""
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'people/person_detail.html', {'person': person})


@login_required
def person_update(request, pk):
    """Update person details (admin only)."""
    person = get_object_or_404(Person, pk=pk)
    
    if request.method == 'POST':
        form = PersonAdminForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save()
            messages.success(request, f'{person.get_full_name()}\'s details have been updated successfully!')
            return redirect('people:detail', pk=person.pk)
    else:
        form = PersonAdminForm(instance=person)
    
    return render(request, 'people/person_update.html', {'form': form, 'person': person})


@login_required
def admin_register(request):
    """Admin-only registration form - simpler interface."""
    if request.method == 'POST':
        form = PersonAdminForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(request, f'{person.get_full_name()} has been registered successfully!')
            return redirect('people:list')
    else:
        form = PersonAdminForm()
    
    return render(request, 'people/admin_register.html', {'form': form})

