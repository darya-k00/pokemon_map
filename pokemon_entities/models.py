from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, blank=False, verbose_name="Имя")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Имя на анг")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Имя на яп")
    image = models.ImageField(blank=True,upload_to='pocemons_images/' null=True, verbose_name="файл картинки")
    previous_evolution = models.ForeignKey('self',
                        on_delete=models.PROTECT,
                        blank=True, null=True,
                        related_name = "next_evolutions",
                        related_query_name = "next_evolutions",
                        verbose_name="Родитель",
                                           )
    description = models.TextField(blank=True, verbose_name="Описание")
    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.PROTECT, null=False,blank=False,
                                related_name="entities",
                                verbose_name='покемон')
    lat = models.FloatField(verbose_name='широта', blank=False,)
    lon = models.FloatField(verbose_name='долгота', blank=False,)
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='появится')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='исчезнет')
    level = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='уровень')
    health = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='здоровье')
    strength = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='атака')
    defence = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='защита')
    stamina = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='выносливость')

    class Meta:
        verbose_name = 'Покемоны на карте'
        verbose_name_plural = 'Покемоны на карте'

    def __str__(self):
        title = '{0} id {1}'.format(self.pokemon.title, self.id)
        return title
