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
from string import join
from math import sqrt, fabs
from PyQt4 import QtCore,QtGui
from antsUI import Ui_MainWindow

# GLOBALS
yvector = [1,0.92,0.7,0.38,0,-0.38,-0.7,-0.92,-1,-0.92,-0.7,-0.38,0,0.38,0.7,0.92]
xvector = [0,-0.38,-0.7,-0.92,-1,-0.92,-0.7,-0.38,0,0.38,0.7,0.92,1,0.92,0.7,0.38]

HDG_RANGE_MASK = 15


# COLOURS
BOUNDARY_C = 0xC80000
BOUNDARY   = QtGui.QColor(BOUNDARY_C)

BACKGROUND_C = 0xFFFFFF
BACKGROUND = QtGui.QColor(BACKGROUND_C)



# ANT CLASS DEFINITION
class Ant:
    def __init__(self, initialx, initialy, hdna, edna, heading, energy, clr):
        self.x = initialx
        self.y = initialy
        self.h = heading
        self.s = 0              # cyclic counter for stepping through the chromosones
        self.colour = clr
        
        # Strength of predation is proportional to the 'redness' of the ant
        self.predator = (clr >> 15) - (((clr >> 8) & 255) + (clr & 255))
        self.energy = energy
        self.dna_feeding = edna[:]
        self.dna_hunting = hdna[:]
        self.next = 0
        
        # path entries: History of recently visited [x-coord, y-coord, underlying pixel colour]
        self.path = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    def __del__(self):
        pass

    def move(self,parent):
        # Move forward one step, including wraparound if the ant reaches the border.
        # Modify the ant's heading using the appropriate DNA strand, depending on 
        #  whether the ant is looking for food or is on a food pixel.
        # Adjust the ant's energy level, and return the new level as the output
        #  of this function.

        # Replace the oldest pixel in the path history (avoids creating infinitely long Ants)
        parent.setPixel(self.path[self.s][0],self.path[self.s][1],self.path[self.s][2])
        
        # Move forward one step on current heading
        self.x += xvector[self.h]
        self.y += yvector[self.h]

        # Work out what the ant has stepped in
        pixel = parent.getPixel(self.x,self.y)
        self.gene = self.dna_hunting[self.s]

        if pixel == BACKGROUND_C or pixel == self.colour:
            pixel = BACKGROUND_C # background is a do-nothing case  
        elif (not(pixel & 0x00FF00FFL)) and (pixel & 0x0000FF00L): # Check for food - eat your greens
            if self.predator <= 0:
                pixel = BACKGROUND_C
                self.energy += FOODENERGY
                self.gene = self.dna_feeding[self.s]
            else:
                pass
            
        elif pixel == BOUNDARY_C:
            pixel = BACKGROUND_C
            limits = parent.mapLimits()
            if self.x <= limits[0]:
                self.x = limits[2]-1
            elif self.x >= limits[2]:
                self.x = limits[0]+1

            if self.y <= limits[1]:
                self.y = limits[3]-1
            elif self.y >= limits[3]:
                self.y = limits[1]+1
        
            # Must be another ant - see if we can eat it
        else: 
            if self.predator > 0:
                try:
                    for prey in parent.ants:
                        if self.predator > prey.predator:
                            for point in prey.path:
                                if (int(point[0]) == int(self.x)) and (int(point[1]) == int(self.y)):
                                    self.energy += prey.energy
                                    prey.energy = -1000  # next time it moves, it's dead
                                    raise StopIteration()
                except StopIteration:
                    pass
            pixel = BACKGROUND_C


        # Manage energy levels - separated for experiments with different energy consumption for predators
        if self.predator > 0:
            self.energy -= 1
        else:
            self.energy -= 1

        if self.energy > MAXENERGY:
            if parent.ui.GluttonyKills.checkState():
                self.energy = 0
            else:
                self.energy = MAXENERGY

        if self.energy <= 0:
            for c in self.path:
                parent.setPixel(c[0],c[1],BACKGROUND_C)
            return 0

        parent.setPixel(self.x,self.y,self.colour)
        self.path[self.s] = [self.x,self.y,pixel]

        self.s += 1
        self.s &= 15


        # work out new heading from gene
        if 'L' == self.gene:
            self.h -= 1
        if 'R' == self.gene:
            self.h += 1
        self.h &= HDG_RANGE_MASK 

        return self.energy


# Return QImage with initialized colour palette
def init_image( width,height ):
    image = QtGui.QImage(width, height, QtGui.QImage.Format_RGB32)
    image.fill(BACKGROUND_C)
    return image

# Paint a blob of vegetation
def vegetate( painter,x,y,r ):
    radialGrad = QtGui.QRadialGradient(QtCore.QPointF(x, y), r);
    radialGrad.setColorAt(0, QtGui.QColor(0,220,0));
    radialGrad.setColorAt(1, QtGui.QColor(0,150,0));
    painter.setBrush(radialGrad)
    painter.setPen(QtGui.QColor(0,150,0))
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
            radius = random.randrange(10,25,4)
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
                    ["FFRRRLLLLLRFLRLR","RRRRLLLLFFFFLLRR"],
                    ["RRRLLLFFFFFFFFFF","RFLRFLLFFFLRFLFR"],
                    ["FFFFFFFLFFFFFFFR","LLLFLLLLFRFFLRRR"],
                    ["FFLFRFRRLLRLFFRL","RRLRLLLLFFLFFLRR"],
                    ["RRRRLLLLFFFFLLRR","FFRRRLLLLLRFLRLR"],
                    ["RRRLLLFFFFFFFFFF","FFFFFFFLFFFFFFFR"],
                    ["RFLRFLLFFFLRFLFR","RRRFLLLLFRFFLRRR"],
                    ["FFLFRFRRLLRLFFRL","RRLRLLLLFFLFFLRR"],
                    ["LLFFFRRFFFLLFFFF","LRLRRLRLLRLRRLRL"]]:
            self.ants.append( Ant( random.randrange(40,self.ui.arena.width()-40),
                                   random.randrange(0,self.ui.arena.height()),
                                   dna[0], dna[1], random.randint(0,HDG_RANGE_MASK), INITIALENERGY,
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

        # new algorithm - ants must be within local radius, requires two loops
        for ant in self.ants:
            energy = ant.move(self)
            if( energy ):
                newlist.append( ant )
                if energy > best[0]:
                    best = [energy,ant]

        self.ants = newlist[:]

        if best[0]:
            for ant in self.ants:
                if  ant.energy > secondbest[0]:
                    distance = int(sqrt((ant.x - best[1].x)*(ant.x - best[1].x) + (ant.y - best[1].y)*(ant.y - best[1].y)))
                    if 0 < distance < 48:
                        secondbest = [ant.energy, ant, distance]

        if best[0] and secondbest[0]:
            # create two new ants
            self.breed(best,secondbest)

        # Revegetate - plant a bud on an existing bit of greenery (if found)
        if random.randint(0,100) > 60: # TODO - make this a panel configuration option
            vx = random.randrange(20,self.ui.arena.width()-20)
            vy = random.randrange(20,self.ui.arena.height()-20)
            vp = self.getPixel(vx,vy)
            if (not(vp & 0x00FF00FFL)) and (vp & 0x0000FF00L): # Check for food - grow your greens
                painter = QtGui.QPainter()
                painter.begin(self.qimg)
                vegetate(painter,vx,vy,10)
                painter.end()

        self.ui.arena.setPixmap(QtGui.QPixmap.fromImage(self.qimg))

    def breed( self, mother, father ):
        # Mother has most energy, so if this test passes, both would pass
        if father[0] < BREEDENERGY:
            return
        
        mhdna = mother[1].dna_hunting
        mfdna = mother[1].dna_feeding
        fhdna = father[1].dna_hunting
        ffdna = father[1].dna_feeding

       
        # zip the genes together
        hh = zip(mhdna,fhdna)
        ff = zip(mfdna,ffdna)
        ah = ''.join("%s%s" % tup for tup in hh[:8] )
        bh = ''.join("%s%s" % tup for tup in hh[8:] )
        af = ''.join("%s%s" % tup for tup in ff[:8] )
        bf = ''.join("%s%s" % tup for tup in ff[8:] )
        
        if self.ui.Mutations.checkState():
            gamma = random.randint(0,1024)
            if gamma & 1:
                self.mutate(ah)
            elif gamma & 8:
                self.mutate(bh)
            elif gamma & 64:
                self.mutate(af)
            elif gamma & 256:
                self.mutate(bf)
        
        energy = (mother[0]+father[0])/8 # some wasted energy 

        mc = self.generate_colour(ah,af)
        fc = self.generate_colour(bh,bf)

        self.ants.append(Ant( mother[1].x, mother[1].y,
                              ah,af,(mother[1].h+1)&HDG_RANGE_MASK, energy, mc ))

        self.ants.append(Ant( mother[1].x, mother[1].y,
                              bh,bf,(father[1].h-1)&HDG_RANGE_MASK, energy, fc ))
    
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
            if hunt[i] == 'L':
                colour |= 1  
            colour *= 2
            if feed[i] == 'R':
                colour |= 1 

        if not( colour & 0x00FF00FFL ):
            colour = 0

        return colour
  
def main():
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.creatant()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
