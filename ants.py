#!/usr/bin/python

import os,sys,random,time
from PyQt4 import QtCore,QtGui
from antsUI import Ui_MainWindow

# GLOBALS
yvector = [1,0.5,0,-0.5,-1,-0.5,0,0.5]
xvector = [0,0.5,1,0.5,0,-0.5,-1,-0.5]
#numants = 0

# CONSTANTS (replace with MainWindow parameters)
FOODENERGY = 18
MAXENERGY  = 900
INITIALENERGY = 280
BREEDENERGY = 600


# COLOURS
BOUNDARY_C = 0xC80000
BOUNDARY   = QtGui.QColor(BOUNDARY_C)

BACKGROUND_C = 0xFFFFFF
BACKGROUND = QtGui.QColor(BACKGROUND_C)

#LIGHTBLUE = QtGui.QColor(0xCCCCFF)
#LIGHTRED  = QtGui.QColor(0xFF8888)
#BLUE      = QtGui.QColor(0x0000FF)
#BROWN     = QtGui.QColor(0xCC6600)
#BLACK     = QtGui.QColor(0x000000)
#CYAN      = QtGui.QColor(0x00FFFF)

LIGHTBLUE = 0xCCCCFF
LIGHTRED  = 0xFF8888
BLUE      = 0x0000FF
BROWN     = 0xCC6600
BLACK     = 0x000000
CYAN      = 0x00FFFF


# ANT CLASS DEFINITION
class Ant:
    def __init__(self, initialx, initialy, initialh, hdna, edna, e, clr):
        #global numants
        self.x = initialx
        self.y = initialy
        self.h = initialh
        self.s = 0
        self.colour = clr
        self.energy = e
        self.dna_feeding = edna[:]
        self.dna_hunting = hdna[:]
        self.next = 0
        self.path = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        #numants += 1

    def __del__(self):
        pass

    def move(self,parent):
        self.path[self.s] = [self.x,self.y]
        self.x += xvector[self.h]
        self.y += yvector[self.h]

        # Work out what the ant has stepped in
        pixel = parent.getPixel(self.x,self.y)

        if (not(pixel & 0x00FF00FFL)) and (pixel & 0x0000FF00L): # Check for food - eat your greens
            self.energy += FOODENERGY
            parent.setPixel(self.x,self.y,BACKGROUND_C)
            self.gene = self.dna_feeding[self.s]

        elif pixel == BOUNDARY_C:
            limits = parent.mapLimits()
            if self.x <= limits[0]:
                self.x = limits[2]-1
            elif self.x >= limits[2]:
                self.x = limits[0]+1

            if self.y <= limits[1]:
                self.y = limits[3]-1
            elif self.y >= limits[3]:
                self.y = limits[1]+1

        else:
            parent.setPixel(self.x,self.y,self.colour)
            self.gene = self.dna_hunting[self.s]

        self.energy -= 1
        self.s += 1
        self.s &= 15
        parent.setPixel(self.path[self.s][0],self.path[self.s][1],BACKGROUND_C)

        # work out new heading from gene
        if 'L' == self.gene:
            self.h -= 1
        if 'R' == self.gene:
            self.h += 1
        self.h &= 7 

        # Manage energy levels
        if self.energy > MAXENERGY:
            self.energy = MAXENERGY

        if self.energy <= 0:
            for c in self.path:
                parent.setPixel(c[0],c[1],BACKGROUND_C)
            return 0

        return self.energy


# Return QImage with initialized colour palette
def init_image( width,height ):
    scale7 = [0,36,72,108,144,180,216,255]
    scale3 = [0,85,170,255]
    image = QtGui.QImage(width, height, QtGui.QImage.Format_RGB32)
    image.fill(BACKGROUND_C)
    return image

# Paint a blob of vegetation
def vegetate( painter,x,y,r ):
    radialGrad = QtGui.QRadialGradient(QtCore.QPointF(x, y), r);
    radialGrad.setColorAt(0, QtGui.QColor(0,100,0));
    radialGrad.setColorAt(1, QtGui.QColor(0,50,0));
    painter.setBrush(radialGrad)
    painter.setPen(QtGui.QColor(0,50,0))
    painter.drawEllipse(x-r,y-r,2*r,2*r)

 

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Create arena image
        self.qimg = init_image(self.ui.arena.width(),self.ui.arena.height())

        self.resetArena()

        self.ui.restart.clicked.connect(self.startAnimation)
        self.ui.reset.clicked.connect(self.resetArena)


    def resetArena(self):
        global FOODENERGY
        global MAXENERGY
        global INITIALENERGY
        global BREEDENERGY

        (MAXENERGY, flump)    = self.ui.maxEnergy.text().toInt()
        (INITIALENERGY, flump)= self.ui.initialEnergy.text().toInt()
        (BREEDENERGY, flump)  = self.ui.breedEnergy.text().toInt()
        (FOODENERGY, flump)   = self.ui.foodEnergy.text().toInt()
        (total_radius, flump) = self.ui.initFood.text().toInt()


        painter = QtGui.QPainter()
        painter.begin(self.qimg)

        # Clear arena
        painter.setBrush(BACKGROUND)
        painter.drawRect(0,0,self.ui.arena.width(),self.ui.arena.height())

        # Draw initial vegetation
        while total_radius > 0:
            radius = random.randrange(10,35,4)
            total_radius -= radius
            vx = random.randrange(0,self.ui.arena.width())
            vy = random.randrange(0,self.ui.arena.height())
            vegetate(painter,vx,vy,radius)

        # Draw arena boundary - avoids doing offscreen lookup for every move
        pen = QtGui.QPen(BOUNDARY, 8, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(4,4,self.ui.arena.width()-4,4)
        painter.drawLine(4,4,4,self.ui.arena.height()-4)
        painter.drawLine(self.ui.arena.width()-4,4,self.ui.arena.width()-4,self.ui.arena.height()-4)
        painter.drawLine(4,self.ui.arena.height()-4,self.ui.arena.width()-4,self.ui.arena.height()-4)
        painter.end
                   
        self.ui.arena.setPixmap(QtGui.QPixmap.fromImage(self.qimg))
        self.creatant()



    def startAnimation(self):
        self.animator=QtCore.QTimer()
        self.animator.timeout.connect(self.animant)
        self.animator.start(20)
        self.ui.restart.clicked.connect(self.stopAnimation)

    def stopAnimation(self):
        self.animator.stop()
        self.ui.restart.clicked.connect(self.startAnimation)


    def getPixel(self,x,y):
        return self.qimg.pixel(x,y) & 0x00ffffffL # mask off alpha(?) byte

    def setPixel(self,x,y,clr):
        self.qimg.setPixel(x,y,clr)

    def mapLimits(self):
        return (8,8,self.ui.arena.width()-8,self.ui.arena.height()-8)

    def creatant(self):
        self.ants = [
                        Ant(200,100,1,"LLFFFFFRFFFRRRLL","RLFRLRRLFRLLRRFR",INITIALENERGY,LIGHTBLUE),
                        Ant(300,200,1,"RRRRLLLLFFFFLLRR","FFRRRLLLLLRFLRLR",INITIALENERGY,LIGHTRED ),
                        Ant(100,100,1,"RRRLLLFFFFFFFFFF","FFFFFFFFFFFFFFFR",INITIALENERGY,BLUE ),
                        Ant(400,200,1,"RFLRFLLFFFLRFLFR","RRRFLLLLFRFFLRRR",INITIALENERGY,BROWN),
                        Ant(250,150,1,"FFLFRFRRLLRLFFRL","RRLRLLLLFFLFFLRR",INITIALENERGY,BLACK),
                        Ant(100,300,1,"LLFFFRRFFFLLFFFF","LRLRRLRLLRLRRLRL",INITIALENERGY,CYAN)
                    ]
        
    def animant(self):
        #print self.ants.__len__()
        newlist = []
        best = [0,0]
        secondbest = [0,0]
        for ant in self.ants:
            energy = ant.move(self)
            if( energy ):
                newlist.append( ant )
                if energy > best[0]:
                    best = [energy,ant]
                elif energy > secondbest[0]:
                    secondbest = [energy,ant]

        self.ants = newlist[:]

        if best[0] and secondbest[0]:
            # create two new ants
            self.breed(best,secondbest)

        #if 98 < random.randrange(0,100):
        vx = random.randrange(40,self.ui.arena.width()-40)
        vy = random.randrange(40,self.ui.arena.height()-40)
        vp = self.getPixel(vx,vy)
        if (not(vp & 0x00FF00FFL)) and (vp & 0x0000FF00L): # Check for food - grow your greens
            painter = QtGui.QPainter()
            painter.begin(self.qimg)
            vegetate(painter,vx,vy,10)
            painter.end()

        self.ui.arena.setPixmap(QtGui.QPixmap.fromImage(self.qimg))

    def breed( self, mother, father ):
        if father[0] < BREEDENERGY:
            print "Breed fail %d %d\n" % (mother[0], father[0])
            return
        ah = []
        bh = []
        af = []
        bf = []
        mhdna = mother[1].dna_hunting
        mfdna = mother[1].dna_feeding
        fhdna = father[1].dna_hunting
        ffdna = father[1].dna_feeding
        
        # zip the genes together
        for i in range(8):
            ah.append( mhdna[i*2]   )
            ah.append( fhdna[i*2+1] )
            bh.append( mhdna[i*2+1] )
            bh.append( fhdna[i*2]   )

            af.append( mfdna[i*2]   )
            af.append( ffdna[i*2+1] )
            bf.append( mfdna[i*2+1] )
            bf.append( ffdna[i*2]   )
        
        energy = (mother[0]+father[0])/6 # some wasted energy 
        #mc = mother[1].colour
        #fc = father[1].colour

        mc = self.generate_colour(ah,af)
        fc = self.generate_colour(bh,bf)

        print "Breeding %x and %x\n" % (mc,fc)        

        self.ants.append(Ant( mother[1].x+(father[1].x-mother[1].x)/10,
                              mother[1].y+(father[1].y-mother[1].y)/10,
                              1,ah,af,energy, mc ))

        self.ants.append(Ant( mother[1].x+(father[1].x-mother[1].x)/5,
                              mother[1].y+(father[1].y-mother[1].y)/5,
                              1,bh,bf,energy, fc ))
    
        mother[1].energy = energy
        father[1].energy = energy

    def generate_colour(self,hunt,feed):
        colour = 0;
        for i in range(12):
            colour *= 2
            if hunt[i] == 'R':
                colour |= 1  
            colour *= 2
            if feed[i] == 'F':
                colour |= 1 

        if not( colour & 0x00FF00FFL ):
            colour = 0

        return colour
  
def main():
    # This is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.creatant()
    window.show()
    window.raise_()

    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
