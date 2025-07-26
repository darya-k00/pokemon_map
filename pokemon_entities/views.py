import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils import timezone

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_enties = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in pokemons_enties:
        pokemon = pokemon_entity.pokemon.title_ru
        if (pokemon_entity.appear_at <= timezone.now()) and (pokemon_entity.disappear_at >= timezone.now()):
            try:
                add_pokemon(
                    folium_map,
                    pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(pokemon_entity.pokemon.images.url)
                )
            except ValueError:
                continue

    pokemons_on_page = []
    for pokemon in pokemons:
        try:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.images.url,
                'title_ru': pokemon.title_ru
            })
        except ValueError:
            continue

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entites = PokemonEntity.objects.filter(pokemon=pokemon)
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entites:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.images.url)
        )

        pokemon_info = {
            'img_url': request.build_absolute_uri(pokemon.images.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,

            'description': pokemon.description
        }

        if pokemon.previous_evolution:
            pokemon_info['previous_evolution'] = {
                'pokemon_id': pokemon.previous_evolution.id,
                'img_url': request.build_absolute_uri(
                    pokemon.previous_evolution.images.url),
                'title_ru': pokemon.previous_evolution.title_ru,
                'title_en': pokemon.previous_evolution.title_en,
                'title_jp': pokemon.previous_evolution.title_jp
            }
        next_evolution = pokemon.next_evolutions.all().first()
        if next_evolution:
            next_evolution = {
                'pokemon_id': next_evolution.id,
                'img_url': request.build_absolute_uri(next_evolution.images.url),
                'title_ru': next_evolution.title_ru
            }
            pokemon_info['next_evolution'] = next_evolution
        

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
