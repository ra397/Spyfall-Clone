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
    
    def join_game(self, game_code, player_name):
        if game_code not in self.games:
            return None, "Game DNE"
        
        player = Player(player_name)
        game = self.games[game_code]
        game.add_player(player)

        return game
    
    def get_game(self, code):
        return self.games[code]