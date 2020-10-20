from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Sum, F
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 

from .models import Team, Player
from .serializer import PlayerSerializer, TeamSerializer
# Create your views here.

cache.set('top10', [])

@api_view(['GET'])
def listPlayer(request):
    queryset = Player.objects.all()
    serializer = PlayerSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def top10(request):
    return Response({'Top10': cache.get('top10')})

@api_view(['GET'])
def team(request, pk):
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
        serializer = PlayerSerializer(queryset)

        return Response(serializer.data)

    if request.method == 'PUT':

        serializer = PlayerSerializer(queryset, data=request.data)

        if queryset.team:
            return Response({ 'error': 'Player is already sold'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid() and serializer.validate(request.data):
            serializer.save()

            team = Team.objects.get(team_no=serializer.data['team'])
            price = serializer.data['price']

            team.budget -= price
            team.save()

            cache.set('top10', [ serializer.data ] + cache.get('top10'))
            print(cache.get('top10'))

            return Response(serializer.data)

        return Response({ 'error': 'Try Again!'}, status=status.HTTP_400_BAD_REQUEST)

    # Doesn't remove the while player, just removes the player from his team
    if request.method == 'DELETE':
        team = queryset.team
        price = queryset.price

        if team:
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

    teams = Player.objects.filter(team__isnull=False).values('team', budget=F('team__budget')).annotate(rating=Sum('player_rating')).order_by('-rating', '-budget')
    
    return Response(teams)