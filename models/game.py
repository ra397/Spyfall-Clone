import random
import string
import time
from models.player import Player
from models.constants import locations_occupations

class Game:
    def __init__(self, owner: Player):
        self.code = self.generate_game_code()
        self.owner = owner
        self.players = [owner]
        self.current_location = None
        self.in_session = False
        self.start_time = None

    def generate_game_code(self, length=5):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def add_player(self, player: Player):
        if self.in_session:
            raise ValueError("Cannot join: round has already started.")
        if any(p.name == player.name for p in self.players):
            raise ValueError(f"Player with {player.name} already exists.")
        self.players.append(player)

    def start(self):
        self.in_session = True
        self.start_time = time.time()
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

    def reset(self):
        self.current_location = None
        self.in_session = False
        self.start_time = None
        for player in self.players:
            player.set_occupation(None)

    def has_started(self):
        return self.in_session
    
    def get_start_time(self):
        return self.start_time

    def get_player_names(self):
        return [player.name for player in self.players]