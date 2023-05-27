import tkinter as tk
from tkinter import ttk
import sv_ttk
import pathlib
from tkinter.filedialog import *


class MainApplication(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        sv_ttk.use_dark_theme()

        self.title("The Sounds of the Future")
        
        # Starts numbers at 1
        self.effect_count = 1
        self.instrument_count = 1
        self.note_count = 1
        
        # theme used: https://github.com/rdbende/Sun-Valley-ttk-theme

        self.create_leftmenu_frame()

        self.create_instrumentframe()
        self.create_effectframe()
        self.create_noteframe()

        self.create_frames()
        self.create_labels()
        self.create_spinboxes()

    def create_spinboxes(self):
        # spinbox for the note # & octave
        self.spinval = tk.StringVar(value="0")
        self.keyselector = ttk.Spinbox(
            self.framenote, from_=0.0, to=127.0, textvariable=self.spinval)
        self.keyselector.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # trace the spinbox value of the note # and octave
        self.spinval.trace("w", lambda x, y, z: self.show_key())
        # spinbox for creating the velocity
        self.velocityval = tk.StringVar(value="0")
        self.velocitybox = ttk.Spinbox(
            self.framenote, from_=0.0, to=127.0, textvariable=self.velocityval)
        self.velocitybox.grid(column=1, row=3, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        self.lengthval = tk.StringVar(value="0")
        self.lengthbox = ttk.Spinbox(
            self.framenote, from_=0.0, to=10000.0, textvariable=self.lengthval, increment=0.1)
        self.lengthbox.grid(column=1, row=5, sticky=(tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

    def create_leftmenu_frame(self):
        # Menu Frame
        self.left_menu_frame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Menu")
        self.left_menu_frame.grid(column=0, row=0, sticky=(
            tk.N, tk.S, tk.W, tk.E), padx=15, pady=15)

        # Add Instrument Button
        self.add_instrument_button = ttk.Button(
            self.left_menu_frame, text="Add Instrument", command=lambda: self.add_instrument())
        self.add_instrument_button.grid(column=1, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Add Note Button
        self.Add_Note_button = ttk.Button(
            self.left_menu_frame, text="Add Note", command=lambda: self.add_note()
        )
        self.Add_Note_button.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Add Effect Button
        self.add_effect_button = ttk.Button(
            self.left_menu_frame, text="Add Effect", command=lambda: self.add_effect())
        self.add_effect_button.grid(column=1, row=2, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Delete Button
        self.delete_button = ttk.Button(
            self.left_menu_frame, text="Delete Selected", command=lambda: self.delete_note())
        self.delete_button.grid(column=1, row=3, sticky=(
            tk.E, tk.W), padx=10, pady=10)

        # Render Button
        self.render_button = ttk.Button(
            self.left_menu_frame, text="Render Audio", command=lambda: self.render())
        self.render_button.grid(column=1, row=4, sticky=(
            tk.E, tk.W), padx=10, pady=(50, 10))

    def create_frames(self):
        # creating the instrument tree on the right
        self.instrument_tree = ttk.Treeview(
            self, show="tree")
        self.instrument_tree.grid(column=2, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)

        self.instrument_tree.tag_configure('instrument', background='green')
        self.instrument_tree.tag_configure('effect', background='orange')
        self.instrument_tree.tag_configure('note', background='green')

        self.instrument_tree.bind(
            "<<TreeviewSelect>>", lambda event: self.tree_select())

    def create_instrumentframe(self):
        # Instrument Frame Construction
        self.frameinstrument = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameINSTRUMENT")
        self.frameinstrument.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

    def create_noteframe(self):
        # Note frame construction
        self.framenote = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameNOTE")
        self.framenote.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

    def create_effectframe(self):
        # Effect frame construction
        self.frameeffect = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameEFFECT")
        self.frameeffect.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

    def create_labels(self):
        # textbox for the velocity of the note
        self.velocitybox_text = tk.Label(
            self.framenote, text="Velocity / Strength", justify="center")
        self.velocitybox_text.grid(column=1, row=2)

        # key label
        self.keyselector_text = ttk.Label(
            self.framenote, text="Note Key", justify="center")
        self.keyselector_text.grid(column=1, row=0)

        self.notelength_text = ttk.Label(
            self.framenote, text="Note Length", justify="center")
        self.notelength_text.grid(column=1, row=4)

    def add_instrument(self):
        self.instrument_tree.insert(
            '', 'end', text="Instrument %d" % (self.instrument_count), tags=["Instrument", self.instrument_count])
        self.instrument_count += 1

    def add_effect(self):
        if (len(self.instrument_tree.selection()) == 0):
            return

        current_selection = self.instrument_tree.selection()[0]

        while (self.instrument_tree.parent(current_selection)):
            current_selection = self.instrument_tree.parent(current_selection)

        self.instrument_tree.insert(current_selection, 'end', text="Effect", tags=[
                                    "effect", self.effect_count])

        self.effect_count += 1

    def add_note(self):
        if (len(self.instrument_tree.selection()) == 0):
            return

        current_selection = self.instrument_tree.selection()[0]

        while (self.instrument_tree.parent(current_selection)):
            current_selection = self.instrument_tree.parent(current_selection)

        self.instrument_tree.insert(current_selection, 'end', text="♪ " + number_to_note(
            int(self.spinval.get())), tags=["note", self.note_count + self.velocity_key + self.length_key])
        self.instrument_tree.tag_configure('note', background='green')
        self.note_count += 1

    def delete_note(self):
        if (len(self.instrument_tree.selection()) == 0):
            return

        for selection in self.instrument_tree.selection():
            self.instrument_tree.delete(selection)

    def render(self):
        asksaveasfile()
        print("renderrenderrender")

    def tree_select(self):
        print(self.instrument_tree.selection()[0])

        sel_id = self.instrument_tree.selection()[0]

        print(self.instrument_tree.item(sel_id))
    def length_key(self):
        self.keyselector.config(float(self.lengthval.get()))

    def velocity_key(self):
        self.keyselector.config(float(self.velocityval.get()))

    def show_key(self):
        self.keyselector_text.config(
            text=number_to_note(int(self.spinval.get())))


def number_to_note(number: int) -> str:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    NOTES_IN_OCTAVE = len(NOTES)

    octave = int(number // NOTES_IN_OCTAVE)
    note = str(NOTES[int(number) % NOTES_IN_OCTAVE])

    return "%s%d" % (note, octave)
