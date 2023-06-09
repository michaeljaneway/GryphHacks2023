from manim import *
from ProjectStructs import *

# This is the class that generates an animation based on file input (audio and JSON)

POINT_SIZE = 0.2
NOTE_WIDTH = 5
NOTE_WIDTH_MULTIPLIER = 1
NOTE_CIRCLE_OFFSET = 1
NOTE_DISTANCE_MULTIPLIER = 4

class AnimationGenerator(Scene):
    def construct(self):
        self.initStartingGraphics()
        self.loadNotes()
        self.initNoteObjects()
        self.startPlaying(self.project.getRuntime())
    
    # all graphics that are not notes
    def initStartingGraphics(self):  
        self.anchorPoints = VGroup()
        anchorP1 = Dot(point=UP * 3, radius = POINT_SIZE)
        anchorP2 = Dot(point=DOWN * 3, radius = POINT_SIZE)
        self.anchorPoints.add(anchorP1, anchorP2)
        
        self.anchorLine = Line(self.anchorPoints[0], self.anchorPoints[1])
        self.anchorLine.color = GREY
                
        # actually added in after notes
        self.topCircle = Circle(color=BLUE_A, fill_opacity=1).surround(anchorP1, buffer_factor=NOTE_WIDTH_MULTIPLIER * 2)
        
        self.add(self.anchorLine)
        
    def addNotes(self, notes):
        self.notes = notes
        self.numNotes = len(self.notes)
    
    # creats all the lines and dots for the note creater
    def initNoteObjects(self):
        self.noteLines = []
        self.endPoints = []
        
        # for loop to count amount of notes on left and amount of notes on right
        notesOnLeft, notesOnRight = self.countNotesOnSides()
        
        curNotesOnLeft = 0
        curNotesOnRight = 0
    
        # sort these notes by their keys (higher notes are supposed to me closer in and lower notes are supposed to be further out)
        # thus lower notes should be earlier in the array as they should be on the outside
        self.notes.sort(key=self.sortByNoteKey, reverse=True)
        
        for i in range(len(self.notes)):
            # every other element goes on left or right side (sorted )
            if i % 2 == 0:
                self.createNote(self.notes[i], curNotesOnLeft/notesOnLeft * NOTE_DISTANCE_MULTIPLIER + 1, LEFT)
                
                curNotesOnLeft += 1
            else:
                self.createNote(self.notes[i], curNotesOnRight/notesOnRight * NOTE_DISTANCE_MULTIPLIER + 1, RIGHT)
                
                curNotesOnRight += 1
            
        self.add(self.topCircle)
        
    def countNotesOnSides(self):
        notesOnLeft = 0
        notesOnRight = 0
        
        # now every other element is added to the right side, first element is on the left
        for i in range(len(self.notes)):
            if i % 2 == 0:
                notesOnLeft += 1
            else:
                notesOnRight += 1
                
        return notesOnLeft, notesOnRight
            
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
        
    # comparison function to sort by a note key
    def sortByNoteKey(self, e):
        return e.key
        
    # calculates horizontal direction
    def calcuateHorizontalDirection(self, side, length):
        return (NOTE_CIRCLE_OFFSET + length) * side
        
    # animates the objects
    def startPlaying(self, duration):
        self.directionsFirst = [] # goes toward center from the left
        self.directionsSecond  = [] # goes away from center to the right
        self.directionsThird = [] # goes toward center from the right
        self.directionsFourth = [] # goes toward the left from the center
        
        i = 0
        
        # assigning the directions to be going to the center (negative x direction)
        for i in range(len(self.endPoints)):
            self.directionsFirst.append([-self.endPoints[i].get_center()[0], -self.endPoints[i].get_center()[1], 0])
            self.directionsSecond.append([-self.endPoints[i].get_center()[0], self.endPoints[i].get_center()[1], 0])
            self.directionsThird.append([self.endPoints[i].get_center()[0], -self.endPoints[i].get_center()[1], 0])
            self.directionsFourth.append([self.endPoints[i].get_center()[0], self.endPoints[i].get_center()[1], 0])
            
            # adjusting to make endpoints go lower
            self.directionsFirst[i] += DOWN * i/self.numNotes
            self.directionsThird[i] += DOWN * i/self.numNotes
            
            self.directionsSecond[i] += UP * i/self.numNotes
            self.directionsFourth[i] += UP * i/self.numNotes
            
            i += 1
            
        animations = []
        
        # for loop to run animations
        for i in range(len(self.endPoints)):
            # dynamically creating a succession of animations for each endpoint and appending them to animations array
            animations.append(self.createAnimationsSuccession(i, duration))

        self.play(*animations)
        
    # creates code for a succession based on time left and full rotations calculated and returns it to be executed
    def createAnimationsSuccession(self, i, duration): 
        timeLeft = duration
        animationDuration = 1 / self.notes[i].frequency # converting from hertz to every x second this occurs
        
        halfAnimationDuration = animationDuration / 2
        animationsAdded = 0
        animationList = []
        
        while animationDuration <= timeLeft:
            # initial view
            # move to right (if endpoint was initially on left), opposite otherwise
            if animationsAdded == 0:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFirst[i], run_time=0, rate_func=rate_functions.linear))       
            # move to right (if endpoint was initially on left), opposite otherwise
            elif animationsAdded % 2 == 1:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsSecond[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsThird[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                timeLeft -= animationDuration
            # move to left (if endpoint was initially on left), opposite otherwise
            else:
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFourth[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                animationList.append(ApplyMethod(self.endPoints[i].shift, self.directionsFirst[i], run_time=halfAnimationDuration, rate_func=rate_functions.linear))
                timeLeft -= animationDuration
                
            animationsAdded += 1
            
        noteSuccession = Succession(*animationList)
        
        return noteSuccession
            
    # creates new line where dot1 is the endpoint (it is presumably getting changed in most cases)
    def getUpdatedLine(self, dot1, dot2):
        point1 = dot1.get_center()
        point2 = dot2.get_center()
        
        updatedLine = Line(point1, point2)
        updatedLine.color = YELLOW
        
        return updatedLine
    
    """The Code Below is Called By The GUI To Render the Project"""
    # loads project provided by GUI
    def load_project(self, project: Project):
        self.project = project

    # loads notes from project provided
    def loadNotes(self):
        Time = ValueTracker()

        notes = []
        # mobject_list = []

        instrument_dict: Dict[str, Instrument] = self.project.getInstruments()

        for instrument_key in instrument_dict:
            note_dict: Dict[str,
                            Note] = instrument_dict[instrument_key].getNotes()

            for note_key in note_dict:
                note = note_dict[note_key] # key as in a dictionary, not the key of the actual note
                
                notes.append(note)
        
        self.addNotes(notes)