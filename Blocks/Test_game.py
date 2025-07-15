from panda3d.core import CollisionBox, CollisionNode


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

class Map:
    def __init__(self):
        self.model = loader.loadModel("Blocks/dirt-block.glb")
        self.land = render.attachNewNode("Land")

    def Create_block(self, position):
        self.block = self.loader.LoadModel(self.model)
        self.block.setPos(position)
        self.block.setPythonTag('type', self.model)
        self.block.reparentTo(self.land)

        hitbox = CollisionBox((-1,-1,-1), (-1,-1,-1))
        blockNode = CollisionNode("block-hitbox")
        blockNode.addSolid(hitbox)
        collider = self.block.attachNewNode(hitbox)
        collider.setPythonTag('owner', self.block)
