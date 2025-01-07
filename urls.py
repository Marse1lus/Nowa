from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='tournaments/home.html'), name='home'),
    path('tournaments/', TemplateView.as_view(template_name='tournaments/turniers.html'), name='tournament_list'),
]

