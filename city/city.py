from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, VBase3, Filename, Fog, Texture, TextureStage, WindowProperties
import os, sys, random
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
    
   
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        wp = WindowProperties() 
        wp.setSize(1024, 768) 
        base.win.requestProperties(wp) 
        
        #Environment
        self.setBackgroundColor(0.3,0.3,1,1) # blue sky
        fog = Fog("fog")
        fog.setColor(0.75,0.75,0.75)
        fog.setExpDensity(0.016)
        self.render.setFog(fog)
        
        # Controls
        self.add_move_key("w", lambda: self.move(y=1))
        self.add_move_key("a", lambda: self.move(x=-1))
        self.add_move_key("d", lambda: self.move(x=1))
        self.add_move_key("s", lambda: self.move(y=-1))
        
        # Camera
        self.disableMouse() 
        self.camera.setPos(12.6694, 16.5869, 2.23608)
        self.camera.setHpr(-5.44159, 7.59898, -0.084791)
        self.taskMgr.add(self.handleMouse, 'mouseStuff')
        
        self.taskMgr.add(self.rotateBuildingColors, 'buildingColors')

        self.cube = loader.loadModel(path_of_local_file("models/cube/cube.egg"))
        self.cube.setScale(0.3,0.3,0.3)
        
        # Floor
        floor_plane = self.cube.copyTo(self.render)
        floor_plane.setScale(100,100,1)
        floor_plane.setColor(0.1,0.75,0.1,1)
        
        # Buildings
        self.buildings = []
        for start_x in range(0,100,20):
            for start_y in range(0,100,25):
                height = random.randrange(5,25)
                color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
                building = self.render.attachNewNode("building")
                
                for y in range(0,10): # west wall
                    for z in range(1,height):
                        self.add_cube(start_x, start_y + y, z,parent=building)
                        
                for y in range(0,10): # east wall
                    for z in range(1,height):
                        self.add_cube(start_x + 10, start_y + y, z, parent=building)
                        
                for x in range(0,11): # north wall
                    for z in range(1,height):
                        self.add_cube(start_x + x, start_y + 10, z, parent=building)
                        
                for x in range(0,11):  # south wall
                    for z in range(1,height):
                        self.add_cube(start_x + x, start_y, z, parent=building)
                
                for c in building.getChildren():
                    gray = random.uniform(0.1,0.4)
                    c.setColor(color[0] - gray,color[1] - gray,color[2] - gray,1)
        
                self.buildings.append(building)
        
        # Trees
        self.tree_model =  loader.loadModel(path_of_local_file("models/plants6/plants6.egg"))
        self.tree_model.setScale(0.25,0.25,0.25)
        for x in range(15,100,20):
            for y in range (15,100,20):
                tree = self.tree_model.copyTo(self.render)
                tree.setPos(x,y,0)
        
        # Roads
        for y in range(15, 100, 20):
            road = self.cube.copyTo(self.render)
            road.setScale(10,100,0.1)
            road.setPos(0,y,0.1)
        
    def add_cube(self,x=0,y=0,z=0,parent=None):
        cube = self.cube.copyTo(self.render)
        cube.setPos(x,y,z)
        if parent: 
            cube.reparentTo(parent) 
        return cube
        
    def printPos(self):
        print "pos = %s" % self.camera.getPos()
        print "hpr = %s" % self.camera.getHpr()
    
    def add_move_key(self, key, function):
        self.accept(key,function)
        self.accept(key+"-repeat",function)
        
    def move(self,x=0,y=0,z=0):
        oldPos = self.camera.getPos()
        oldPos.addX(x)
        oldPos.addY(y)
        oldPos.addZ(z)
        self.camera.setPos(oldPos)
    
    def rotate(self,h=0,p=0,r=0):
        oldHpr = self.camera.getHpr()
        oldHpr.addX(h)
        oldHpr.addY(p)
        oldHpr.addZ(r)
        self.camera.setHpr(oldHpr)
    
    def handleMouse(self, task):
        md = base.win.getPointer( 0 ) 
        x = md.getX()
        y = md.getY()
        
        centerx = self.win.getXSize() / 2.0
        centery = self.win.getYSize() / 2.0
        factor = 0.1
        
        if self.win.movePointer(0, centerx, centery):
            deltaHeading = ( x - centerx ) * factor
            deltaPitch = ( y - centery ) * factor
            self.rotate(-1*deltaHeading,deltaPitch)
        return Task.cont
    
    def rotateBuildingColors(self, task):
        for b in self.buildings:
            for c in b.getChildren():
                oldColor = c.getColor()
                delta = random.uniform(-0.25,0.25)
                c.setColor(oldColor[0]+delta, oldColor[1]+delta,  oldColor[2]+delta, 1)
        
        task.delayTime = 2
        return Task.again
        
def path_of_local_file(name):
    mydir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
    mydir = Filename.fromOsSpecific(mydir).getFullpath() # Convert that to panda's unix-style notation.
    return mydir + "/" + name
    
app = MyApp()
app.run()