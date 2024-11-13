from random import randint

class Dice:
    def __init__(self, FaceList: list = [1, 2, 3, 4, 5, 6]):
        self.face = {
            "1": FaceList[0],
            "2": FaceList[1],
            "3": FaceList[2],
            "4": FaceList[3],
            "5": FaceList[4],
            "6": FaceList[5]
        }

    def get_dice(self):
        return self.face[str(randint(1, 6))]
    
    def alternative_button(self):
        while True:
            if input("請按ENTER擲骰子") == "":
                return True
            else:
                print("您按的不是ENTER")
    

if __name__ == "__main__":
    a = Dice()
    print(a.get_dice())
