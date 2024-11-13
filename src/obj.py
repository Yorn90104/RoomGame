class Person:
    def __init__(self, name: str = "",  play: bool = False):
        self.name = name
        self.alive = True #存活狀態
        self.player = play #是否為玩家
        self.codename = None
        self.current_room = None  # 當前所在房間
        self.substitute_times = 3 #可使用替身次數
    
    def __str__(self) -> str:
        return self.name

class Room:
    def __init__(self, name: str = "", *neighbor_rooms):
        self.name = name
        self.neighbor_room = tuple(neighbor_rooms) #鄰近房間
        self.inside = list() 

    def __str__(self) -> str:
        return self.name

    def enter_room(self, person: Person):
        """進入房間"""
        self.inside.append(person)
        person.current_room = self

    def leave_room(self, person: Person):
        """離開房間"""
        self.inside.remove(person)

    def survive_people_inside(self):
        return list(p for p in self.inside if p.alive == True)

    def judge_people_inside(self):
        """判斷房間裡面是否有人"""
        return (len(self.survive_people_inside()) > 0)
            
    def judge_people_neighbor(self):
        """判斷鄰近房間是否有人"""
        return any(room.judge_people_inside() for room in self.neighbor_room)