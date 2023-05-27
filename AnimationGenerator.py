from manim import *
from ProjectStructs import Note
from random import randint

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.2
NOTE_WIDTH = 5
NOTE_WIDTH_MULTIPLIER = 1
NOTE_CIRCLE_OFFSET = 2

class AnimationGenerator(Scene):
    def construct(self):
        self.initStartingGraphics()
        self.initNotes()
        self.startPlaying()
    
    # all graphics that are not notes
    def initStartingGraphics(self):
        self.plane = NumberPlane() # to remove
        self.add(self.plane)        
        
        self.anchorPoints = VGroup()
        anchorP1 = Dot(point=UP * 3, radius = POINT_SIZE)
        anchorP2 = Dot(point=DOWN * 3, radius = POINT_SIZE)
        self.anchorPoints.add(anchorP1, anchorP2)
        
        self.anchorLine = Line(self.anchorPoints[0], self.anchorPoints[1])
        self.anchorLine.color = RED
                
        self.topCircle = Circle().surround(anchorP1, buffer_factor=NOTE_WIDTH_MULTIPLIER * 2)
        self.topCircle.set_stroke(color=PINK)
        
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
                
        # iterates through each note that will be put on the left
        notesOnSide = 0
        
        for i in range(self.startLeft, self.endLeft):
            self.createNote(self.notes[i], notesOnSide + 1, LEFT)
            notesOnSide += 1
            
        # puts rest of notes on the right
        notesOnSide = 0
        
        for i in range(self.startRight, self.endRight):
            self.createNote(self.notes[i], notesOnSide + 1, RIGHT)
            notesOnSide += 1
            
    # creates a new note line and note end point (p1)
    def createNote(self, note, length, side):
        # adding note lines
        notePoints = VGroup()
        noteP1 = Dot(point=UP * 3 + self.calcuateHorizontalDirection(side, length), radius=POINT_SIZE)
        noteP2 = Dot(point=UP * 3, radius=POINT_SIZE)
        
        notePoints.add(noteP1, noteP2)
        noteLine = Line(noteP1, noteP2)
        noteLine.color = YELLOW
        
        # noteP2.add_updater((lambda dot: dot.become(self.getUpdatedEndDot(noteP2, note.freqency))))
        noteLine.add_updater((lambda line: line.become(self.getUpdatedLine(noteP1, noteP2))))
        
        self.noteLines.append(noteLine)
        self.endPoints.append(noteP1)
        
        self.add(noteLine)
        
    # calculates horizontal direction
    def calcuateHorizontalDirection(self, side, length):
        return (NOTE_CIRCLE_OFFSET + length) * side
        
    # animates the objects
    def startPlaying(self):
        directions = []
        
        # assigning the directions to be going to the center (negative x direction)
        for dot in self.endPoints:
            directions.append([-dot.get_center()[0], -dot.get_center()[1], 0])
            
        animations = []
        
        for dot, direction, note in zip(self.endPoints, directions, notes):
            print(note.frequency)
            animations.append(ApplyMethod(dot.shift, direction, run_time=note.frequency * 3))
            
        self.play(*animations)
            
    # creates new line where dot1 is the endpoint (it is presumably getting changed in most cases)
    def getUpdatedLine(self, dot1, dot2):
        point1 = dot1.get_center()
        point2 = dot2.get_center()
        
        updatedLine = Line(point1, point2)
        updatedLine.color = YELLOW
        
        return updatedLine
    
    # updates the center of the end point and returns and updated position, given a certain frequency
    def getUpdatedEndDot(self, endDot, frequency):
        pointLocation = endDot.get_center()
        
        # noteP1 = Dot(point=UP * 3 + self.calcuateHorizontalDirection(side, length), radius=POINT_SIZE)
        
        print(pointLocation)
    
if __name__ == "__main__":
    # creating notes to test
    notes = []
    
    for i in range(6):
        # frequency right now is half of the note
        # key (to change later) and frequency are the most relevant
        noteToAdd = Note("", randint(0, 127), i, 0, 0)
        notes.append(noteToAdd)
    
    scene = AnimationGenerator()
    scene.addNotes(notes)
    scene.render()