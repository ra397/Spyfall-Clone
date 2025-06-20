import random
import string
from models.player import Player
from models.constants import locations_occupations

class Game:
    def __init__(self, owner: Player):
        self.code = self.generate_game_code()
        self.owner = owner
        self.players = [owner]
        self.current_location = None

    def generate_game_code(self, length=5):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def add_player(self, player: Player):
        if any(p.name == player.name for p in self.players):
            raise ValueError(f"Player with {player.name} already exists.")
        self.players.append(player)

    def start(self):
        self.current_location = random.choice(list(locations_occupations.keys()))
        occupations = locations_occupations[self.current_location][:]
        spy = random.choice(self.players)
        random.shuffle(self.players)
        for player in self.players:
            if player is spy:
                player.set_occupation("spy")
            else:
                if occupations:
                    player.current_occupation = occupations.pop()
                else:
                    player.current_occupation = "bystander" # if we run out of occupations
    def get_player_names(self):
        player_names = []
        for player in self.players:
            player_names.append(player.name)
        return player_names