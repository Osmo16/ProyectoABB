print("hola")

class Node:
    def __init__(self, poder, name, x=0, y=0):
        self.power = poder
        self.name = name
        self.x = x
        self.y = y
        self.left = None
        self.right = None