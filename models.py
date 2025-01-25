from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tournament(models.Model):
    TOURNAMENT_STATUS = [
        ('upcoming', 'Предстоящий'),
        ('ongoing', 'Текущий'),
        ('completed', 'Завершенный'),
    ]

    TOURNAMENT_TYPES = [
        ('greco', 'Греко-римская борьба'),
        ('freestyle', 'Вольная борьба'),
        ('judo', 'Дзюдо'),
        ('bjj', 'BJJ'),
    ]

    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TOURNAMENT_STATUS, default='upcoming')
    registration_deadline = models.DateTimeField(default=timezone.now)
    max_participants = models.IntegerField(default=100)
    current_participants = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization_name = models.CharField(max_length=255)
    company_info = models.TextField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='tournament_images/', blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TOURNAMENT_TYPES, default='greco')

    def __str__(self):
        return self.name

    @property
    def is_registration_open(self):
        return timezone.now() <= self.registration_deadline and self.current_participants < self.max_participants

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tournament')
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"

