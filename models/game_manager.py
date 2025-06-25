from models.game import Game
from models.player import Player

class GameManager:
    def __init__(self):
        self.games = {} # game_code -> Game

    def create_game(self, owner_name):
        player = Player(owner_name)
        game = Game(player)
        self.games[game.code] = game
        return game
    
    def join_game(self, code, player_name):
        if code not in self.games:
            return None, "Game DNE"

        game = self.games[code]
        if game.has_started():
            return None, "Game already started"

        if player_name in game.get_player_names():
            return None, "Name already taken"

        player = Player(player_name)
        game.add_player(player)
        return game, None
    
    def get_game(self, code):
        return self.games[code]