from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from . import models

def home_template_view(request,player):
    """Serves the home.djhtml template from /e/macid/<player>
    Parameters
    ----------
    request : (HttpResponse) should be a simple Http GET with no arguments

    Returns
    -------
    out : (HttpResponse) renders the home.djhtml template

    """
    try:
        player_o = models.Player.objects.get(name__iexact=player)
        player_games = player_o.games.all()

        # lookup the name (String value) of the players favourite console
        fav_console_name = ''

        # lookup the number of games player plays that are on their favourite console
        num_games_fav = 0

        # lookup all a list of all companies player has bought games from
        companies = []

        # lookup a list of all games both player and Jimmy play
        pj_games = []

        # lookup all consoles that have a newer generation that players favourite console
        fav_gen = 0
        newer_consoles = []

        # lookup all games player plays that are available on all 3 platforms (Nintendo,Microsoft,Sony)
        all_platforms = []

        # lookup all players that have a game in common with player
        common_players = []

        context = { 'player_name' : player_o.name
                    ,'fav_console' : fav_console_name
                    ,'num_games_fav' : num_games_fav
                    ,'companies' : companies
                    ,'pj_games' : pj_games
                    ,'fav_gen' : fav_gen
                    ,'newer_consoles' : newer_consoles
                    ,'all_platforms' : all_platforms
                    ,'common_players' : common_players }
        return render(request,'home.djhtml',context)

    except ObjectDoesNotExist:
        return HttpResponseNotFound("ObjectDoesNotExist raised when looking up %s" % (player))
