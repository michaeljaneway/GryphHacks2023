from manim import *
from ProjectStructs import Note

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.08
NOTE_WIDTH = 5
NOTE_WIDTH_MULTIPLIER = 2
NOTE_CIRCLE_OFFSET = 2

"""
Outline of solution to move objects.

Use updater function in provided link -- have a lambda function that updates the line with the new update (does this every frame)
Also add an updater function with a lambda for updating the endpoint (p1) on the circle. Updates it so that new circle still surrounds it.
"""

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
        
        # self.anchorLine.add_updater()
        # self.update_self()
                
        self.topCircle = Circle().surround(anchorP1, buffer_factor=NOTE_WIDTH_MULTIPLIER * 2)
        self.topCircle.set_stroke(color=PINK)
        
        self.add(self.anchorLine)
        self.add(self.topCircle)
        
    def addNotes(self, notes):
        self.notes = notes
        self.numNotes = len(self.notes)
    
    def initNotes(self):
        self.noteLines = []
        self.noteCircles = []
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
            
    # creates a new note line and note circle
    def createNote(self, note, length, side):
        # adding note lines
        notePoints = VGroup()
        noteP1 = Dot(point=UP * 3 + self.calcuateHorizontalDirection(side, length), radius=POINT_SIZE)
        noteP2 = Dot(point=UP * 3, radius=POINT_SIZE)
        
        notePoints.add(noteP1, noteP2)
        noteLine = Line(noteP1, noteP2)
        noteLine.color = YELLOW
        
        noteLine.add_updater((lambda line: line.become(self.getUpdatedLine(noteP1, noteP2))))
        
        # adding note circles
        noteCircle = Circle().surround(noteP1, buffer_factor = NOTE_WIDTH_MULTIPLIER)
        noteCircle.set_stroke(color=ORANGE)
        
        # noteCircle.add_updater((lambda circle: circle.become(self.getUpdatedCircle(noteP1))))
        
        self.noteLines.append(noteLine)
        self.noteCircles.append(noteCircle)
        self.endPoints.append(noteP1)
        
        self.add(noteLine)
        self.add(noteCircle)
        
    # calculates horizontal direction
    def calcuateHorizontalDirection(self, side, length):
        return (NOTE_CIRCLE_OFFSET + length) * side
        
    # animates the objects
    def startPlaying(self):
        # runs dynamically craeted code to animate the objects
        exec(self.createPendulumCode())
        
    # creates the pendulum code and returns it -- this is dynamically created and run by an exec function
    def createPendulumCode(self):
        pendulumAnimationCode = "self.play("
        
        # shifts endpoints (set of P1s)
        for i in range(self.startLeft, self.endLeft):
            pendulumAnimationCode += "self.endPoints["
            pendulumAnimationCode += str(i)
            pendulumAnimationCode += "].animate.shift(DOWN + LEFT),"
        
        for i in range(self.startRight, self.endRight):
            pendulumAnimationCode += "self.endPoints["
            pendulumAnimationCode += str(i)
            pendulumAnimationCode += "].animate.shift(DOWN + RIGHT),"
        
        pendulumAnimationCode += " run_time=3)"
                
        return pendulumAnimationCode
    
    # creates new line where dot1 is the endpoint (it is presumably getting changed in most cases)
    def getUpdatedLine(self, dot1, dot2):
        point1 = dot1.get_center()
        point2 = dot2.get_center()
        
        updatedLine = Line(point1, point2)
        updatedLine.color = YELLOW
        
        return updatedLine
    
    # creats a new circle and returns it, given the updated point (updated endpoint, which corresponds to P1)
    def getUpdatedCircle(self, endDot):
        endPoint = endDot.get_center()
        
        updatedCircle = Circle().surround(endDot, buffer_factor = NOTE_WIDTH_MULTIPLIER)
        updatedCircle.set_stroke(color=ORANGE)
        
        return updatedCircle
        
    
if __name__ == "__main__":
    # creating notes to test
    notes = []
    
    for i in range(6):
        # frequency right now is half of the note
        noteToAdd = Note(i/2, i)
        notes.append(noteToAdd)
    
    scene = AnimationGenerator()
    scene.addNotes(notes)
    scene.render()