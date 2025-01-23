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

    title = models.CharField(max_length=200, verbose_name='Название турнира')
    tournament_type = models.CharField(max_length=20, choices=TOURNAMENT_TYPES, verbose_name='Тип турнира')
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    start_date = models.DateTimeField(verbose_name='Дата начала', default=timezone.now)
    end_date = models.DateTimeField(verbose_name='Дата окончания', default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    status = models.CharField(max_length=20, choices=TOURNAMENT_STATUS, default='upcoming', verbose_name='Статус')
    registration_deadline = models.DateTimeField(verbose_name='Дедлайн регистрации', default=timezone.now)
    max_participants = models.IntegerField(verbose_name='Максимальное количество участников', default=100)
    current_participants = models.IntegerField(default=0, verbose_name='Текущее количество участников')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'

    def __str__(self):
        return self.title

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
        return f"{self.user.username} - {self.tournament.title}"

