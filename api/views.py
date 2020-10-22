from django.shortcuts import render
from django.db.models import Sum, F, Case, When
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 

import json

from .models import Team, Player, Top10
from .serializer import PlayerSerializer, TeamSerializer, Top10Serializer
# Create your views here.


@api_view(['GET'])
def listPlayer(request):
    """
    Return the list the list of all player queryset in the database
    :param : Django request
    :return : JSON object of array of player querysets
    """

    queryset = Player.objects.all()
    serializer = PlayerSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def top10(request):
    """
    Return the list of player dicitionary, which contains the latest player that have been sold
    :param : Django request
    :return : JSON object of array of player dictionary 
    """

    queryset = Top10.objects.all()
    serializer = Top10Serializer(queryset.first())
    return Response(serializer.data)

@api_view(['GET'])
def team(request, pk):
    """
    Return the Team informations based on the primary key
    :param : Django request, primary key 
    :return : JSON object of a Team queryset
    """

    team = Team.objects.get(team_no=pk)
    players = Player.objects.filter(team=pk)

    team_serializer = TeamSerializer(team)
    player_serializer = PlayerSerializer(players, many=True)

    return Response({'team': team_serializer.data , 'players': player_serializer.data })

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def assignTeam(request, pk):

    queryset = Player.objects.get(pk=pk)

    if request.method == 'GET':
        """
        Returns individual player information, based on the primary key
        """
        serializer = PlayerSerializer(queryset)

        return Response(serializer.data)

    if request.method == 'PUT':
        """
        Update the team & price field of the player, based on the primary key
        Returns the updated player 
        """
        serializer = PlayerSerializer(queryset, data=request.data)

        # Update Player only if the player doesn't belong to a team
        if queryset.team:
            return Response({ 'error': 'Player is already sold'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid() and serializer.validate(request.data):
            serializer.save()

            team = Team.objects.get(team_no=serializer.data['team'])
            price = serializer.data['price']

            # Reducing the budget of the team
            team.budget -= price
            team.save()

            # Updating the Top10 list
            queryset = Top10.objects.all().first()
            queryset.top10 = ([json.dumps(serializer.data)] + queryset.top10)[:10]
            queryset.save()

            return Response(serializer.data)

        return Response({ 'error': 'Try Again!'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        """
        Removes the player from his team, and decrease his price to zero
        Returns the updated player
        """
        team = queryset.team
        price = queryset.price

        if team:
            # Adding the price of the player to the team, which had bought the player
            team.budget += price 
            team.save()
             
            queryset.price = 0 
            queryset.team = None 
            queryset.save() 

        serializer = PlayerSerializer(queryset)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def leaderboard(request):
    """
    :param : Django request
    :return : JSON object of a array of team dictionary which contains, team_no, budget and the rating of the team
    """
    
    teams = Player.objects.filter(team__isnull=False).values('team', budget=F('team__budget')).annotate(rating=Sum('player_rating')).order_by('-rating', '-budget')

    return Response(teams)