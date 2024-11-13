import random
import string
import time
from src.dice import Dice
from src.obj import Person, Room

class RoomGame:
    def __init__(self):
        #創建房間
        self.mid_room = Room("Mid_Room")
        self.red_room = Room("Red_Room")
        self.yellow_room = Room("Yellow_Room")
        self.blue_room = Room("Blue_Room")
        self.green_room = Room("Green_Room")

        self.rooms = [self.mid_room, self.red_room, self.yellow_room, self.blue_room, self.green_room] # 房間列表

        #設置鄰近房間
        self.red_room.neighbor_room = (self.mid_room, self.blue_room, self.green_room)
        self.yellow_room.neighbor_room = (self.mid_room, self.green_room, self.blue_room)
        self.blue_room.neighbor_room = (self.mid_room, self.yellow_room, self.red_room)
        self.green_room.neighbor_room = (self.mid_room, self.yellow_room, self.red_room)
        
        #參與者 participant
        self.participant_strict = 20
        self.participant_dict = dict() #參與者名單字典

        self.code_names = list(string.ascii_uppercase) #創建代碼表

        #骰子
        self.color_dice = Dice([
                "Black",
                "Red",
                "Yellow",
                "Green",
                "Blue",
                "Black"
                ])
        
        self.color = None #擲出顏色

        self.what = True #隨便用的

    def player_survive_over_one(self):
        """判斷是否有玩家有超過一個存活"""
        return (len(self.player_survive_list()) > 1)
    
    def participant_survive_list(self):
        """存活的參與者名單"""
        return list(p for p in self.participant_dict if self.participant_dict[p].alive == True)
    
    def player_survive_list(self):
        """存活的玩家名單"""
        return list(p for p in self.participant_dict if self.participant_dict[p].player == True and self.participant_dict[p].alive == True)
    
    def npc_survive_list(self):
        """存活的 NPC 名單"""
        return list(p for p in self.participant_dict if self.participant_dict[p].player == False and self.participant_dict[p].alive == True)

    def add_player_participant(self, *players):
        """添加玩家參與者"""
        #玩家
        for player_name in players:
            self.participant_dict[str(player_name)] = Person(str(player_name), True)

        players_num = len(self.participant_dict) #玩家人數
        print(f"已加入 {players_num}位玩家：")
        print(", ".join([str(self.participant_dict[n]) for n in self.participant_dict]))

        #非玩家

        for i in range(1, self.participant_strict - players_num + 1):
            self.participant_dict[f"NPC_{i}"] = Person(f"NPC_{i}")

    def assign_codename(self):
        """分配代號""" 
        random.shuffle(self.code_names)  # 隨機打亂代號順序

        code_index = 0

        for p in self.participant_dict:
            self.participant_dict[p].codename = self.code_names[code_index]
            code_index += 1
    
    def display_codename(self):
        """展示玩家代號"""
        print("---將顯示玩家的代號---\n(請記住自己的代號)")
        for player in self.player_survive_list():
            # 查看代號的三個步驟
            for i in range(3):
                if i == 0:
                    info = f"查看 {player} 的代號"
                elif i == 1:
                    info = f"{player} 的代號為：{self.participant_dict[player].codename} "
                elif i == 2:
                    info = f"已查看完 {player} 的代號 "
                
                for i in range(10):
                    print(f'\r{info} (倒數 {10 - i } 秒) ', end='                               ')
                    time.sleep(1)
            print(f'\r{info}', end='                               ')
            print()

    def codename_find_name(self, codename: str):
        """代號 查找 參與者名"""
        return next((self.participant_dict[p].name for p in self.participant_survive_list() if self.participant_dict[p].codename == codename), None)


    def assign_rooms(self):
        """將參與者隨機分配到不同房間，每個房間最多 participant_strict / 5 個人"""
        all_participants = list(self.participant_dict[p] for p in self.participant_dict) 
        random.shuffle(all_participants)  # 隨機打亂所有參與者

        for room in self.rooms:
            for _ in range(self.participant_strict // 5):
                if len(all_participants) > 0:
                    participant = all_participants.pop()
                    room.enter_room(participant)
                else:
                    break

    def change_room(self, person: Person, new_room: Room):
        """改變參與者的所在房間"""
        person.current_room.leave_room(person)
        new_room.enter_room(person)

    def print_room_structure(self):
        """列印房間構造"""
        self.what = True
        print("     ┌──────────────────┐┌────────┐")
        print("     │ Yellow Room      ││ Blue   │")
        print("     │                  ││ Room   │")
        print("     └──────────────────┘│        │")
        print("     ┌────────┐┌────────┐│        │")
        print("     │ Green  ││Mid Room││        │")
        print("     │ Room   ││        ││        │")
        print("     │        ││        ││        │")
        print("     │        ││        ││        │")
        print("     │        │└────────┘└────────┘")
        print("     │        │┌──────────────────┐")
        print("     │        ││    Red Room      │")
        print("     │        ││                  │")
        print("     └────────┘└──────────────────┘")

    def print_room_information(self, info):
        """顯示所有房間的指定資訊"""
        self.print_room_structure()

        print("-" * 25)
        for room in self.rooms:
            try:
                print(f"{room.name}：", ", ".join([getattr(p, info) for p in room.inside if p.alive == True]))
            except AttributeError:
                print(f"屬性 '{info}' 不存在")
                
        print("-" * 25)
    
    def get_color_dice(self):
        """擲顏色骰子"""
        self.color = self.color_dice.get_dice()
        print(f"擲出顏色：{self.color}\n")
        

    def judge_color(self, player):
        """判斷顏色(目前執行玩家)"""
        if self.color == "Black":
            self.black_kill(player)
        else:
            self.color_move(player)

    def npc_substitute(self, player):
        """NPC 替身"""
        if len(self.npc_survive_list()) == 0:
            return None
        
        while self.participant_dict[player].substitute_times > 0:
            ans = input(f"是否使用 NPC 替身：\n(最多使用 3 次，剩餘 {self.participant_dict[player].substitute_times} 次)\nYes: 1 No: 0\n")
            if ans == "1":
                print(f"{player} 使用NPC替身")
                substitute = random.choice(self.npc_survive_list())
                self.participant_dict[player].substitute_times -= 1
                return substitute
            elif ans == "0":
                print(f"{player} 不使用NPC替身")
                return None
            else:
                print("輸入錯誤\n")

        return None

    def black_kill(self, player):
        """黑色_選擇殺死同房間的一個參與者(目前執行玩家)"""
        s = self.npc_substitute(player) #使用npc替身
        if s != None:
            self.participant_dict[s].alive = False
            print(f"{s} (代號 {self.participant_dict[s].codename} )已死亡")
            print(f"剩餘存活玩家：", ", ".join(self.player_survive_list()))
            return

        if len(self.participant_dict[player].current_room.survive_people_inside()) == 1:
            print("同房間僅剩自己\n請自殺")
            self.participant_dict[player].alive = False
            print(f"{player} (代號 {self.participant_dict[player].codename} )已死亡")
            print(f"剩餘存活玩家：", ", ".join(self.player_survive_list()))
            return
        
        while True:
            victim_codename = input("選擇殺死同房間的一個人\n請輸入其代號：\n")
            
            victim_name = self.codename_find_name(victim_codename)

            if victim_name == None:
                print("無法找到該代號的參與者，請重新輸入！\n")

            elif self.participant_dict[victim_name].current_room == self.participant_dict[player].current_room : #判斷是否同一房間
                self.participant_dict[victim_name].alive = False
                print(f"{victim_name} (代號 {self.participant_dict[victim_name].codename} )已死亡")
                print(f"剩餘存活玩家：", ", ".join(self.player_survive_list()))
                break
            else:
                print("該代號的參與者與您不同房間\n請重新輸入！")

    def color_move(self, player):
        """移動一個參與者， 移入 擲出顏色的房間 or 移出 擲出顏色的房間(目前執行玩家)"""
        while True:
            ans = input(f"請選擇：\n將一名參與者移入 {self.color}_Room：1  將一名參與者移出 {self.color}_Room：0\n")
            now_room = next((room for room in self.rooms if room.name == f"{self.color}_Room"), None)


            if ans == "1":
                if now_room.judge_people_neighbor() == False:
                    print("鄰近房間內沒有參與者，無法選擇移入\n")
                    continue
                print("\n已選擇移入")
                
                while True:
                    #列印鄰近房間資訊
                    for room in now_room.neighbor_room:
                        print("-" * 25)
                        print(f"{room.name}：", ", ".join([p.codename for p in room.survive_people_inside()]))
                        print("-" * 25)

                    moved_codename = input(f"選擇一名參與者，輸入其代號：\n")

                    moved_name = self.codename_find_name(moved_codename)

                    if moved_name == None:
                        print("無法找到該代號的參與者，請重新輸入！\n")
                    
                    elif any(self.participant_dict[moved_name].current_room == room for room in now_room.neighbor_room): #判斷是否在鄰近房間內
                        print(f"{player} 將 {moved_codename} 從 {self.participant_dict[moved_name].current_room} 移動至 {now_room.name}")
                        self.change_room(self.participant_dict[moved_name], now_room)
                        return

                    else:
                        print("該代號的參與者不鄰近的房間內，請重新輸入！\n")
            
            elif ans == "0":
                if now_room.judge_people_inside() == False:
                    print("該房間內沒有參與者，無法選擇移出\n")
                    continue

                print("\n已選擇移出")
                while True:
                    #列印當前房間資訊
                    print("-" * 25)
                    print(f"{now_room.name}：", ", ".join([p.codename for p in now_room.inside if p.alive == True]))
                    print("-" * 25)

                    moved_codename = input(f"選擇一名參與者，輸入其代號：\n")
                    moved_name = self.codename_find_name(moved_codename)

                    if moved_name == None:
                        print("無法找到該代號的參與者，請重新輸入！\n")
                    
                    elif self.participant_dict[moved_name].current_room == now_room : #判斷是否在房間內
                        while True:
                            #列印可至房間
                            for i in range(len(now_room.neighbor_room)):
                                print(f"{now_room.neighbor_room[i].name}: {i+1}")

                            goal_room_str = input(f"選擇一個鄰近房間：\n")

                            try:
                                goal_room_index = int(goal_room_str) - 1
                            except:
                                print("輸入有誤 請輸入整數數字！!\n")
                                continue

                            if 0 <= goal_room_index < len(now_room.neighbor_room):
                                print(f"{player} 將 {moved_codename} 從 {now_room.name} 移動至 {now_room.neighbor_room[goal_room_index].name}")
                                self.change_room(self.participant_dict[moved_name], now_room.neighbor_room[goal_room_index])
                                return
                            else:
                                print("輸入有誤 請重新輸入！\n")

                    else:
                        print(f"該代號的參與者不在{now_room.name}房間內，請重新輸入！\n")

            else:
                print("輸入錯誤\n")

                    

    def judge_game_over(self):
        """判斷遊戲結束"""
        if self.player_survive_over_one() == False:
            print("\n---遊戲結束---")
            print(f"{self.player_survive_list()[0]}獲勝！")
            return True
        else:
            return False
            
            

    
