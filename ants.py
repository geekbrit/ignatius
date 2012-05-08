#!/usr/bin/python

#----------------------------------------------------------------------
#   ants.py
#       Simulation of population growth and genetic evolution
#       with user-settable energy supply profiles.
#
#   Author: Peter Maloy
#           geekbrit@gmail.com
#
#   No rights reserved.
#
#----------------------------------------------------------------------

import os,sys,random,time
from PyQt4 import QtCore,QtGui
from antsUI import Ui_MainWindow

# GLOBALS
yvector = [1,0.5,0,-0.5,-1,-0.5,0,0.5]
xvector = [0,0.5,1,0.5,0,-0.5,-1,-0.5]


# COLOURS
BOUNDARY_C = 0xC80000
BOUNDARY   = QtGui.QColor(BOUNDARY_C)

BACKGROUND_C = 0xFFFFFF
BACKGROUND = QtGui.QColor(BACKGROUND_C)



# ANT CLASS DEFINITION
class Ant:
    def __init__(self, initialx, initialy, hdna, edna, e, clr):
        self.x = initialx
        self.y = initialy
        self.h = 1
        self.s = 0
        self.colour = clr
        self.energy = e
        self.dna_feeding = edna[:]
        self.dna_hunting = hdna[:]
        self.next = 0
        self.path = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    def __del__(self):
        pass

    def move(self,parent):
        self.path[self.s] = [self.x,self.y]
        self.x += xvector[self.h]
        self.y += yvector[self.h]

        self.gene = self.dna_hunting[self.s]

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
            if parent.ui.GluttonyKills.checkState():
                self.energy = 0
            else:
                self.energy = MAXENERGY

        if self.energy <= 0:
            for c in self.path:
                parent.setPixel(c[0],c[1],BACKGROUND_C)
            return 0

        return self.energy


# Return QImage with initialized colour palette
def init_image( width,height ):
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
        self.ants = []
        for dna in [["LLFFFFFRFFFRRRLL","RLFRLRRLFRLLRRFR"],
                    ["RRRRLLLLFFFFLLRR","FFRRRLLLLLRFLRLR"],
                    ["RRRLLLFFFFFFFFFF","FFFFFFFLFFFFFFFR"],
                    ["RFLRFLLFFFLRFLFR","RRRFLLLLFRFFLRRR"],
                    ["FFLFRFRRLLRLFFRL","RRLRLLLLFFLFFLRR"],
                    ["LLFFFRRFFFLLFFFF","LRLRRLRLLRLRRLRL"]]:
            self.ants.append( Ant( random.randrange(40,self.ui.arena.width()-40),
                                   random.randrange(0,self.ui.arena.height()),
                                   dna[0], dna[1], INITIALENERGY,
                                   self.generate_colour( dna[0], dna[1] )
                                 )
                            )
       
    def animant(self):
        if 2 > self.ants.__len__():
            self.stopAnimation()
            return
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

        # Revegetate - plant a bud on an existing bit of greenery (if found)
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
            #print "Breed fail %d %d\n" % (mother[0], father[0])
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

        if self.ui.Mutations.checkState():
            gamma = random.randint(0,255)
            if gamma & 1:
                self.mutate(ah)
            if gamma & 4:
                self.mutate(bh)
            if gamma & 16:
                self.mutate(af)
            if gamma & 64:
                self.mutate(bf)
        
        energy = (mother[0]+father[0])/8 # some wasted energy 
        #mc = mother[1].colour
        #fc = father[1].colour

        mc = self.generate_colour(ah,af)
        fc = self.generate_colour(bh,bf)

        #print "Breeding %x and %x\n" % (mc,fc)        

        self.ants.append(Ant( mother[1].x+(father[1].x-mother[1].x)/100,
                              mother[1].y+(father[1].y-mother[1].y)/100,
                              ah,af,energy, mc ))

        self.ants.append(Ant( mother[1].x+(father[1].x-mother[1].x)/200,
                              mother[1].y+(father[1].y-mother[1].y)/200,
                              bh,bf,energy, fc ))
    
        mother[1].energy = energy
        father[1].energy = energy

    def mutate(self,dna):
        index = random.randint(0,15)
        if dna[index] == 'L':
            dna[index] = 'F'
        elif dna[index] == 'R':
            dna[index] = 'F'
        elif dna[index] == 'F':
            if index & 1:
                dna[index] = 'R'
            else:
                dna[index] = 'L'

    def generate_colour(self,hunt,feed):
        colour = 0;
        for i in range(12):
            colour *= 2
            if hunt[i] == 'R':
                colour |= 1  
            colour *= 2
            if feed[i] == 'L':
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
