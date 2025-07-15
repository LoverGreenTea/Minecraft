from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import Vec3

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

game = Game()
game.run()
