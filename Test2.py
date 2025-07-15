from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import Vec3

from Test_game import Map

class Game(ShowBase):
    def __init__(self):
        super().__init__(self)
        map = Map()
        map.Create_block((0, 0, 0))
        map.Create_block((0, 0, 2))
        ShowBase.__init__(self)

game = Game()
game.run()
