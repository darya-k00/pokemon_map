from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200,
                                verbose_name='имя покемона на русском',
                                blank=True
                                )
    title_en = models.CharField(blank=True,
                                max_length=200,
                                verbose_name='имя покемона на английском'
                                )
    images = models.ImageField(blank=True,
                               null=True,
                               upload_to='pocemons_images/',
                               verbose_name='изображение покемона'
                               )
    description = models.TextField(blank=True, verbose_name='описание')
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.CASCADE,
                                           null=True, blank=True,
                                           related_name='next_evolutions',
                                           verbose_name='предыдущая эволюция покемона'
                                           )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон',
        related_name='entities'
        )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appear_at = models.DateTimeField(verbose_name='дата и время появления')
    disappear_at = models.DateTimeField(blank=True,
                                        null=True,
                                        verbose_name='дата и время исчезновения'
                                        )
    level = models.PositiveIntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.PositiveIntegerField(null=True, blank=True, verbose_name="Здоровье")
    strength = models.PositiveIntegerField(null=True, blank=True, verbose_name="Атака")
    defence = models.PositiveIntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.PositiveIntegerField(null=True, blank=True, verbose_name="Выносливость")
# your models here
