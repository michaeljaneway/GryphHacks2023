from manim import *
from ProjectStructs import Note
from random import randint

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.2
NOTE_WIDTH = 5
NOTE_WIDTH_MULTIPLIER = 1
NOTE_CIRCLE_OFFSET = 1
NOTE_DISTANCE_MULTIPLIER = 4

class AnimationGenerator(Scene):
    def construct(self):
        self.initStartingGraphics()
        self.initNotes()
        scene.startPlaying(23)
    
    # all graphics that are not notes
    def initStartingGraphics(self):  
        self.anchorPoints = VGroup()
        anchorP1 = Dot(point=UP * 3, radius = POINT_SIZE)
        anchorP2 = Dot(point=DOWN * 3, radius = POINT_SIZE)
        self.anchorPoints.add(anchorP1, anchorP2)
        
        self.anchorLine = Line(self.anchorPoints[0], self.anchorPoints[1])
        self.anchorLine.color = GREY
                
        self.topCircle = Circle(color=BLUE_A, fill_opacity=1).surround(anchorP1, buffer_factor=NOTE_WIDTH_MULTIPLIER * 2)
        
        self.add(self.anchorLine)
        self.add(self.topCircle)
        
    def addNotes(self, notes):
        self.notes = notes
        self.numNotes = len(self.notes)
    
    def initNotes(self):
        self.noteLines = []
        self.endPoints = []
        
        # determining indices for which what goes on the left and what goes on the right
        self.startLeft = 0
        self.endLeft = int(self.numNotes/2)
        self.startRight = self.endLeft
        self.endRight = self.numNotes
        notesOnLeft = self.endLeft - self.startLeft
        notesOnRight = self.endRight - self.startRight
                
        # iterates through each note that will be put on the left
        notesOnSide = 0
        
        for i in range(self.startLeft, self.endLeft):
            self.createNote(self.notes[i], notesOnSide/notesOnLeft * NOTE_DISTANCE_MULTIPLIER + 1, LEFT)
            notesOnSide += 1
            
        # puts rest of notes on the right
        notesOnSide = 0
        
        for i in range(self.startRight, self.endRight):
            self.createNote(self.notes[i], notesOnSide/notesOnRight * NOTE_DISTANCE_MULTIPLIER + 1, RIGHT)
            notesOnSide += 1
            
    # creates a new note line and note end point (p1)
    def createNote(self, note, length, side):
        # adding note lines
        notePoints = VGroup()
        noteP1 = Dot(point=UP * 2 + self.calcuateHorizontalDirection(side, length), radius=POINT_SIZE)
        noteP2 = Dot(point=UP * 3, radius=POINT_SIZE)
        
        notePoints.add(noteP1, noteP2)
        noteLine = Line(noteP1, noteP2)
        noteLine.color = YELLOW
        
        noteLine.add_updater((lambda line: line.become(self.getUpdatedLine(noteP1, noteP2))))
        
        self.noteLines.append(noteLine)
        self.endPoints.append(noteP1)
        
        self.add(noteLine)
        
    # calculates horizontal direction
    def calcuateHorizontalDirection(self, side, length):
        return (NOTE_CIRCLE_OFFSET + length) * side
        
    # animates the objects
    def startPlaying(self, duration):
        self.directionsFirst = [] # goes toward center from the left
        self.directionsSecond  = [] # goes away from center to the right
        self.directionsThird = [] # goes toward center from the right
        self.directionsFourth = [] # goes toward the left from the center
        
        # assigning the directions to be going to the center (negative x direction)
        for dot in self.endPoints:
            self.directionsFirst.append([-dot.get_center()[0], -dot.get_center()[1], 0])
            self.directionsSecond.append([-dot.get_center()[0], dot.get_center()[1], 0])
            self.directionsThird.append([dot.get_center()[0], -dot.get_center()[1], 0])
            self.directionsFourth.append([dot.get_center()[0], dot.get_center()[1], 0])
            
        animations = []
        
        # for loop to run animations
        for i in range(len(self.endPoints)):
            # dynamically creating a succession of animations for each endpoint and appending them to animations array
            animations.append(self.createAnimationsSuccession(i, duration))

        self.play(*animations)
        
    # creates code for a succession based on time left and full rotations calculated and returns it to be executed
    def createAnimationsSuccession(self, i, duration): 
        timeLeft = duration
        animationDuration = self.notes[i].frequency
        halfAnimationDuration = animationDuration / 2
        animationsAdded = 0
        animationList = []
        
        while animationDuration <= timeLeft:
            # initial view
            # move to right (if endpoint was initially on left), opposite otherwise
            if animationsAdded == 0:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFirst[i], run_time=self.notes[i].frequency, rate_func=rate_functions.linear),)       
            # move to right (if endpoint was initially on left), opposite otherwise
            elif animationsAdded % 2 == 1:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsSecond[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsThird[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
            # move to left (if endpoint was initially on left), opposite otherwise
            else:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFourth[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFirst[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
     
            animationsAdded += 1
            timeLeft -= animationDuration
            
        noteSuccession = Succession(*animationList)
        
        return noteSuccession
            
    # creates new line where dot1 is the endpoint (it is presumably getting changed in most cases)
    def getUpdatedLine(self, dot1, dot2):
        point1 = dot1.get_center()
        point2 = dot2.get_center()
        
        updatedLine = Line(point1, point2)
        updatedLine.color = YELLOW
        
        return updatedLine
    
if __name__ == "__main__":
    # creating notes to test
    notes = []
    
    for i in range(15):
        # frequency right now is half of the note
        # key (to change later) and frequency are the most relevant
        noteToAdd = Note("", randint(0, 127), i + 2, 0, 0)
        notes.append(noteToAdd)
    
    scene = AnimationGenerator()
    scene.addNotes(notes)
    scene.render()