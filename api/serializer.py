from rest_framework import serializers 
from .models import Team, Player, Top10

TEAM_FORMAT = {
    'Batsmen': 4,
    'Spin Bowler': 2,
    'Pace Bowler': 2,
    'All Rounder': 2,
    'Wicket Keeper': 1,
}

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def validate(self, data):
        team_no = str(data['team'])
        price = data['price']
        player_type = data['player_type']

        team = Team.objects.get(team_no=team_no)
        players_of_input_type = Player.objects.filter(team=team_no, player_type=player_type).count()

        print(price, team.budget)

        if price <= team.budget and players_of_input_type < TEAM_FORMAT[player_type]:
            return data

        raise serializers.ValidationError("Cannot buy this player.")
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team 
        fields = '__all__'
 
class Top10Serializer(serializers.ModelSerializer):
    class Meta:
        model = Top10
        fields = '__all__'