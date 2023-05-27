import tkinter as tk
from tkinter import ttk
import sv_ttk
import pathlib
from tkinter.filedialog import *


class MainApplication(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        sv_ttk.use_dark_theme()

        self.title("The Sounds of the Future")

        # theme used: https://github.com/rdbende/Sun-Valley-ttk-theme
        self.create_frames()
        self.create_buttons()
        self.create_labels()
        self.create_spinboxes()
        self.create_instrumentframe()
        self.create_effectframe()
        self.create_noteframe()
        
    def create_spinboxes(self):
        #spinbox for the note # & octave
        self.spinval = tk.StringVar(value="0")
        self.keyselector = ttk.Spinbox(
            self.framemid, from_=0.0, to=127.0, textvariable=self.spinval)
        self.keyselector.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        
        #trace the spinbox value of the note # and octave
        self.spinval.trace("w", lambda x, y, z: self.show_key())
        #spinbox for creating the velocity
        self.velocityval = tk.StringVar(value="0")
        self.velocitybox = ttk.Spinbox(
            self.framemid, from_=0.0, to=127.0, textvariable=self.velocityval)
        self.velocitybox.grid(column=1, row=3, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        
    def create_frames(self):
        #creating the left frame
        self.frameleft = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameLEFT")
        self.frameleft.grid(column=0, row=0, sticky=(
            tk.N, tk.S, tk.W, tk.E), padx=15, pady=15)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        
        self.testbutton1 = ttk.Button(self.frameleft,text="Hide Mid",command=lambda: self.hide_mid_frame())
        self.testbutton2 = ttk.Button(self.frameleft,text="Show Mid",command=lambda: self.show_mid_frame())
        self.testbutton1.grid(column=0, row=100)
        self.testbutton2.grid(column=0, row=101)
        
        # Starts numbers at 1 
        self.effect_count = 1
        self.instrument_count = 1
        self.note_count = 1
        #creating the instrument tree on the right
        self.instrument_tree = ttk.Treeview(
            self)
        self.instrument_tree.grid(column=2, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)

        self.instrument_tree.insert('', 'end', 'Instr1', text="Instrument 1")
        self.instrument_tree.insert('Instr1', 'end', text="Note 1")
        self.instrument_tree.insert('Instr1', 'end', text="Note 2")
        self.instrument_tree.insert('Instr1', 'end', text="Effect 1")
        self.instrument_tree.insert('Instr1', 'end', text="Effect 2")

        self.instrument_tree.insert('', 'end', text='swag', tags=('swag'))
        self.instrument_tree.tag_configure('swag', background='green')
        self.instrument_tree.tag_bind(
            'swag', "<1>", self.instrument_tree.focus())

        self.instrument_tree.bind(
            "<<TreeviewSelect>>", lambda event: self.tree_select())
        
    def create_instrumentframe(self):
        #Instrument Frame Construction
        self.frameinstrument = ttk.LabelFrame(
        self, padding="20", width=150, height=200, text="FrameINSTRUMENT")
        self.framemid.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        
    def create_noteframe(self):
        #Note frame construction
        self.framenote = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameNOTE")
        self.framemid.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        
    def create_effectframe(self):
        #Effect frame construction
        self.frameeffect = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameEFFECT")
        self.framemid.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        
    def create_buttons(self):
        #add an instrument Button
        self.add_instrument_button = ttk.Button(self.frameleft,text="Add Instrument",command=lambda: self.add_instrument())
        self.add_instrument_button.grid(column=0,row=0,sticky=(tk.N,tk.W,tk.E,tk.S),padx=10,pady=10)

        #button for rendering audio
        self.render_button = ttk.Button(
            self.frameleft, text="Render Audio", command=lambda: self.render())
        self.render_button.grid(column=0, row=3, sticky=(
            tk.E, tk.W), padx=50, pady=66)
        
        #delete a note Button
        self.delete_button = ttk.Button(
            self.frameleft, text="Delete Selected", command=lambda: self.delete_note())
        self.delete_button.grid(column=0, row=1, sticky=(
            tk.E, tk.W), padx=10, pady=10)
        
        #add a note Button
        self.Add_Note_button = ttk.Button(
            self.frameleft, text="Add Note", command=lambda: self.add_note()
        )
        self.Add_Note_button.grid(column=2, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)


        # self.countryvar = tk.StringVar()
        # self.country = ttk.Combobox(self.<WHICHFRAME?>, textvariable=self.countryvar)
        # self.country.grid(column=0,row=1)

    def create_labels(self):
        #textbox for the velocity of the note
        self.velocitybox_text = tk.Label(
            self.framenote, text="Velocity", justify="center")
        self.velocitybox_text.grid(column=1, row=2)

        #key label
        self.keyselector_text = ttk.Label(
            self.framenote, text="Note Key", justify="center")
        self.keyselector_text.grid(column=1, row=0)
        
    def add_instrument(self):
        self.instrument_tree.insert('', 'end', text="Instrument %d" % (self.instrument_count) )
        self.instrument_count += 1
    
    def add_note(self):
        current_selection = self.instrument_tree.selection()[0]
        
        while (self.instrument_tree.parent(current_selection)):
            current_selection = self.instrument_tree.parent(current_selection)
        
        self.instrument_tree.insert(current_selection, 'end', text=number_to_note(int(self.spinval.get())), tags=["note", self.note_count])
        self.note_count += 1
        
    

    def delete_note(self):
        self.instrument_tree.delete(self.instrument_tree.focus())

    def render(self):
        asksaveasfile()
        print("renderrenderrender")

    def tree_select(self):
        print("Selected_obj")

    def show_key(self):
        self.keyselector_text.config(
            text=number_to_note(int(self.spinval.get())))


def number_to_note(number: int) -> str:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVES = list(range(11))
    NOTES_IN_OCTAVE = len(NOTES)

    octave = int(number // NOTES_IN_OCTAVE)
    note = str(NOTES[int(number) % NOTES_IN_OCTAVE])

    return "NOTE = %s%d" % (note, octave)
