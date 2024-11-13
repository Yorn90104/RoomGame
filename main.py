
from src.logic import Game, begin

while True:
    players = input("請輸入玩家名(請以空白間隔, 至少 2 名玩家)：").split()
    if len(players) >= 2:
        break
    else:
        print("玩家數量不足，請至少輸入 2 名玩家。")

Game.add_player_participant(*players)
Game.assign_codename()
Game.display_codename()
Game.assign_rooms()

begin()


