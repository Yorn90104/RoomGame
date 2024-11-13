from src.game import RoomGame

Game = RoomGame()


def begin():
    while Game.player_survive_over_one():

        for player in Game.player_survive_list() :
            if Game.participant_dict[player].alive == False: #如果輪到此回合已死玩家
                break

            Game.print_room_information("codename")
            print(f"---輪到{player}擲骰子---")
            if Game.color_dice.alternative_button():
                Game.get_color_dice()
                Game.judge_color(player)

            if Game.judge_game_over():
                break


