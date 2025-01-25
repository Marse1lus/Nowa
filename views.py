from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from .models import Tournament
from .forms import TournamentForm, UserRegisterForm
from django.utils import timezone
from django.http import JsonResponse

def home(request):
    return render(request, 'tournaments/home.html')

class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/turniers.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        queryset = Tournament.objects.all()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def post(self, request, *args, **kwargs):
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament_list')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TournamentForm()
        return context

def tournament_list(request):
    status = request.GET.get('status')
    query = request.GET.get('query')
    type = request.GET.get('type')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    tournaments = Tournament.objects.all().order_by('registration_deadline')

    if status:
        tournaments = tournaments.filter(status=status)
    if query:
        tournaments = tournaments.filter(name__icontains=query)
    if type:
        tournaments = tournaments.filter(type=type)
    if start_date and end_date:
        tournaments = tournaments.filter(start_date__gte=start_date, end_date__lte=end_date)

    data = {
        'tournaments': list(tournaments.values('name', 'location', 'start_date', 'end_date', 'registration_deadline', 'image'))
    }
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tournaments/register.html', {'form': form})

def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Турнир успешно создан!')
            return redirect('tournament_list')
        else:
            print("Форма не прошла валидацию:", form.errors)
    else:
        form = TournamentForm()
    return render(request, 'tournaments/create.html', {'form': form})

def register_event(request):
    if request.method == 'POST':
        tournament = Tournament(
            name=request.POST.get('name'),
            date=request.POST.get('date'),
            location=request.POST.get('location'),
            description=request.POST.get('description'),
            organization_name=request.POST.get('organizationName'),
            company_info=request.POST.get('companyInfo'),
            first_name=request.POST.get('firstName'),
            last_name=request.POST.get('lastName'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postalCode'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phoneNumber'),
            status=request.POST.get('status', 'upcoming'),
            registration_deadline=request.POST.get('registration_deadline', timezone.now()),
            max_participants=request.POST.get('max_participants', 100),
            current_participants=0
        )
        tournament.save()
        messages.success(request, 'Турнир успешно зарегистрирован!')
        return redirect('tournament_list')
    else:
        return redirect('home')
