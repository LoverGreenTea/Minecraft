from math import sin, cos


from direct import task
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import  ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionNode, CollisionHandlerQueue, CollisionTraverser, DirectionalLight, \
    AmbientLight, TransparencyAttrib

from Map import Map

def degToRad(degrees):
    return degrees * (3.14 / 180.0)

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)
        self.map = Map()
        self.map.create_block((0,0,0))
        self.map.model = 'Blocks/stone-block.glb'
        self.map.create_block((0, 0,2))
        self.setupCamera()
        self.setupControls()
        self.map.load_map()
        self.SetupLight()
        self.SetupSkyBox()
        self.SetupCrosshairs()
        self.taskMgr.add(self.update, 'update')

    def delete_block(self):
        if self.ray_queue.getNumEntries() >0:
            self.ray_queue.sortEntries()
            ray_hit = self.ray_queue.get_entry(0)

            hit_node = ray_hit.GetIntoNodePath()
            hit_object = hit_node.getPythonTag('owner')


    def create_block(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            ray_hit = self.ray_queue.get_entry(0)

            hit_node = ray_hit.getIntoNodePath()
            hit_object = hit_node.getPythonTag('owner')

            pos = hit_object.getPos()
            normal = ray_hit.getSurfaceNormal(hit_node)
            new_pos = pos + normal*2
            self.map.create_block(new_pos)


    def update(self, task):
        dt = globalClock.getDt()

        speed = 10
        x = y = z = 0
        if self.key_map["forward"]:
            x -= dt * speed * sin(degToRad(self.camera.getH()))
            y += dt * speed * cos(degToRad(self.camera.getH()))
        if self.key_map['backward']:
            x += dt * speed * sin(degToRad(self.camera.getH()))
            y -= dt * speed * cos(degToRad(self.camera.getH()))
        if self.key_map['left']:
            x -= dt * speed * cos(degToRad(self.camera.getH()))
            y -= dt * speed * sin(degToRad(self.camera.getH()))
        if self.key_map['right']:
            x += dt * speed * cos(degToRad(self.camera.getH()))
            y += dt * speed * sin(degToRad(self.camera.getH()))
        #if self.key_map['up']:
            #z += dt * speed
        #if self.key_map['down']:
            #z -= dt * speed
        #self.camera.setPos(
            self.camera.setPos(
                self.camera.getX() + x,
                self.camera.getY() + y,
                self.camera.getZ() + z,
            )

        cursor = self.win.getPointer(0)
        cursor_x = cursor.getX()
        cursor_y = cursor.getY()

        cursor_dx = cursor_x - (self.win.getXSize() // 2)
        cursor_dy = cursor_y - (self.win.getYSize() // 2)
        self.camera.setHpr(
            self.camera.getH() - cursor_dx * dt *2,
            self.camera.getP() - cursor_dy * dt *2, 0
        )
        self.win.movePointer(0, self.win.getXSize() // 2,self.win.getYSize() // 2)
        return task.cont
    def update_move(self, key, value):
        self.key_map[key] = value


    def setupControls(self):
        self.key_map = {
            "forward": False,
            "backward": False,
            "left": False,
            'right': False,


        }
        self.accept('d', self.update_move, ['right', True])
        self.accept('a', self.update_move, ['left', True])
        self.accept('w', self.update_move, ['forward', True])
        self.accept('w-up', self.update_move, ['forward', False])
        self.accept('mouse3', self.create_block)
        self.accept('mouse1', self.delete_block)
        self.accept('v', self.map.save_map)
        self.accept('1', self.setGrassBlock)

    def setGrassBlock(self):
        self.map.model = "blocks/grass-block.glb"

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, -10, 0)
        self.camLens.setFov(80)

        ray = CollisionRay()
        ray.setFromLens(self.cam.node(), 0, 0)

        rayNode = CollisionNode('ray')
        rayNode.addSolid(ray)

        rayNodePath = self.camera.attachNewNode(rayNode)

        self.ray_queue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(rayNodePath, self.ray_queue)

    def SetupLight(self):
        main_light = DirectionalLight('main light')
        main_light_node = render.attachNewNode(main_light)
        main_light_node.setHpr(30, -70, 0)
        render.setLight(main_light_node)

        ambient_light = AmbientLight('ambient_light')
        ambient_light_node = render.attachNewNode(ambient_light)
        ambient_light_node.setColor((0.3, 0.3, 0.3, 1))
        render.setLight(ambient_light_node)

    def SetupCrosshairs(self):
        crosshair = OnscreenImage(
            image='crosshairs.png',
            pos=(0,0,0),
            scale=0.05
        )
        crosshair.setTransparency(TransparencyAttrib.MAlpha)

    def SetupSkyBox(self):
        skybox = loader.loadModel('SkyBlocks/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)
game = Game()
game.run()