from manim import *
from manim.camera.camera import Camera
from ProjectStructs import Note

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.08
NOTE_WIDTH = 5

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
        
        self.topCircle = Circle().surround(anchorP1, buffer_factor=4)
        self.topCircle.set_stroke(color=PINK)
        
        self.add(self.anchorLine)
        self.add(self.topCircle)
        
    def addNotes(self, notes):
        self.notes = notes
        self.numNotes = len(self.notes)
    
    def initNotes(self):
        self.noteLines = []
        self.noteCircles = []
        
        # determining indices for which what goes on the left and what goes on the right
        startLeft = 0
        endLeft = int(self.numNotes/2)
        startRight = endLeft
        endRight = self.numNotes
                
        # iterates through each note that will be put on the left
        notesOnSide = 0
        
        for i in range(startLeft, endLeft):
            self.createNote(self.notes[i], notesOnSide + 1, LEFT)
            notesOnSide += 1
            
        # puts rest of notes on the right
        notesOnSide = 0
        
        for i in range(startRight, endRight):
            self.createNote(self.notes[i], notesOnSide + 1, RIGHT)
            notesOnSide += 1
            
    # creates a new note line and note circle
    def createNote(self, note, length, side):
        notePoints = VGroup()
        noteP1 = Dot(point=UP * 3 + side * length, radius=POINT_SIZE)
        noteP2 = Dot(point=UP * 3, radius=POINT_SIZE)
        
        notePoints.add(noteP1, noteP2)
        noteLine = Line(noteP1, noteP2)
        noteLine.color = YELLOW
        
        self.add(noteLine)
        self.noteLines.append(noteLine)
        
    def startPlaying(self):
        for i in self.noteCircles:
            pass
    
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