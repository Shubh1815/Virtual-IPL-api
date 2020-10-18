from django.urls import path 
from .views import listPlayer, team, assignTeam, top10, leaderboard

urlpatterns = [
    path('top10/', top10, name="Top 10"),
    path('leaderboard/', leaderboard, name="Leaderboard"),
    path('player/', listPlayer, name="List-Player"),
    path('player/<int:pk>/', assignTeam, name="Assign-Team"),
    path('team/<int:pk>/', team, name="Team"),
]