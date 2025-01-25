from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournament_list'),
    path('create/', views.create_tournament, name='create'),
    path('register/', views.register, name='register'),
    path('register-event/', views.register_event, name='register_event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


