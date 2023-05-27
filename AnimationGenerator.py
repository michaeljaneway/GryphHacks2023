from manim import *
from manim.camera.camera import Camera
from ProjectStructs import Note

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.08
NOTE_WIDTH = 5

"""
Note about notes:
Note will hold frequency, key (actual note being played)
"""

class AnimationGenerator(Scene):
    def construct(self):
        tempNumNotes = 1 # to be removed once I start parsing a JSON file
        self.initStartingGraphics()
        self.initNotes(tempNumNotes)
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
    
    def initNotes(self, numNotes):
        self.noteCircles = []
        
        for i in range(numNotes):
            self.noteCircles.append(Circle())
    
            self.noteCircles[i].set_stroke(color=PINK, width=NOTE_WIDTH)
            # self.add(self.noteCircles[i])
    
    def startPlaying(self):
        for i in self.noteCircles:
            pass
    
if __name__ == "__main__":
    # creating notes to test
    notes = []
    
    for i in range(5):
        # frequency right now is half of the note
        noteToAdd = Note(i/2, i)
        notes.append(noteToAdd)
    
    scene = AnimationGenerator()
    scene.addNotes(notes)
    scene.render()