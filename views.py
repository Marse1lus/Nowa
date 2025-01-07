from django.shortcuts import render
from django.views.generic import ListView
from .models import Tournament

def home(request):
    return render(request, 'tournaments/home.html')

class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/tournament_list.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        queryset = Tournament.objects.all()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
