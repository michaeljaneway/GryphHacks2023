import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
import sv_ttk
from tkinter.filedialog import *
from typing import *

import os

from SoundGenerator import SoundGenerator

from ProjectStructs import *

from AnimRenderScene import AnimRenderScene

# converts a number in the spinbox to it's respective note


def number_to_note(number: int) -> str:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    NOTES_IN_OCTAVE = len(NOTES)

    octave = int(number // NOTES_IN_OCTAVE)
    note = str(NOTES[int(number) % NOTES_IN_OCTAVE])

    return "%s%d" % (note, octave)


class MainApplication(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Set dark theme
        sv_ttk.use_dark_theme()

        # Set Window title
        self.title("The Sounds of the Future")

        # Dict to hold every project
        self.projects: Dict[str, Project] = {}

        self.current_selection_struct = None

        # theme used: https://github.com/rdbende/Sun-Valley-ttk-theme

        # create initial frames
        self.create_leftmenu_frame()
        self.create_projectframe()
        self.create_instrumentframe()
        self.create_effectframe()
        self.create_noteframe()
        self.create_tree()

# Constructors
    # creates the menuframe on the left hand side of the screen
    def create_leftmenu_frame(self):
        # Menu Frame
        self.left_menu_frame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Menu")
        self.left_menu_frame.grid(column=0, row=0, sticky=(
            tk.N, tk.S, tk.E, tk.W), padx=15, pady=15)

        # Add Project Button
        self.add_project_button = ttk.Button(
            self.left_menu_frame, text="Add Project", command=lambda: self.add_project())
        self.add_project_button.grid(column=1, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Add Instrument Button
        self.add_instrument_button = ttk.Button(
            self.left_menu_frame, text="Add Instrument", command=lambda: self.add_instrument())
        self.add_instrument_button.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Add Note Button
        self.add_Note_button = ttk.Button(
            self.left_menu_frame, text="Add Note", command=lambda: self.add_note())
        self.add_Note_button.grid(column=1, row=2, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Add Effect Button
        self.add_effect_button = ttk.Button(
            self.left_menu_frame, text="Add Effect", command=lambda: self.add_effect())
        self.add_effect_button.grid(column=1, row=3, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        # Delete Button
        self.delete_button = ttk.Button(
            self.left_menu_frame, text="Delete Selected", command=lambda: self.selected_note_delete())
        self.delete_button.grid(column=1, row=4, sticky=(
            tk.E, tk.W), padx=10, pady=10)

        # Render Button
        self.render_button = ttk.Button(
            self.left_menu_frame, text="Render Audio", command=lambda: self.render())
        self.render_button.grid(column=1, row=5, sticky=(
            tk.E, tk.W), padx=10, pady=(50, 10))

    # Creates the Project/Instrument/Note Tree on the right side of the screen
    def create_tree(self):
        self.tree = ttk.Treeview(
            self, show="tree")
        self.tree.grid(column=2, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)

        self.tree.bind("<<TreeviewSelect>>", lambda event: self.tree_select())

    # Creates the Project frame in the middle.
    def create_projectframe(self):
        # ==========================================================
        # Project Frame
        # ==========================================================

        self.projectFrame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Project")

        # ==========================================================
        # Project Variables
        # ==========================================================

        # Variables

        self.projectFrame_vars: Dict[str, tk.StringVar] = {

            "sample_rate": tk.StringVar(),
            "runtime": tk.StringVar()
        }

        # Variable trace callbacks

        for key in self.projectFrame_vars:
            self.projectFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_project_vals())

        # ==========================================================
        # Create Project Widgets
        # ==========================================================

        # Key Label
        sampleRate_Label = ttk.Label(
            self.projectFrame, text="Sample Rate (Hz)")

        # Velocity Label
        runtime_Label = ttk.Label(
            self.projectFrame, text="Runtime (s)")

        # Spinbox for note # and octave
        sampleRate_Spinbox = ttk.Spinbox(
            self.projectFrame, from_=0.0, to=1000000.0, textvariable=self.projectFrame_vars["sample_rate"])

        # Velocity Spinbox
        runtime_Spinbox = ttk.Spinbox(
            self.projectFrame, from_=0.0, to=1000000.0, textvariable=self.projectFrame_vars["runtime"])

        # ==========================================================
        # Grid Project Widgets
        # ==========================================================

        sampleRate_Label.grid(column=0, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        sampleRate_Spinbox.grid(column=0, row=1, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        runtime_Label.grid(column=0, row=2, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        runtime_Spinbox.grid(column=0, row=3, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

    def create_instrumentframe(self):
        # ==========================================================
        # Instrument Frame
        # ==========================================================

        self.instrumentFrame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Instrument")

        # ==========================================================
        # Instrument Variables
        # ==========================================================

        # Variables
        self.instrumentFrame_vars: Dict[str, tk.StringVar] = {
            "instrument_path": tk.StringVar()
        }

        # Variable trace callbacks

        for key in self.instrumentFrame_vars:
            self.instrumentFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_instrument_vals())

        # ==========================================================
        # Create Instrument Widgets
        # ==========================================================

        # Path Label
        pathlabel = ttk.Label(
            self.instrumentFrame, text="Instrument path", justify="center")

        # Entry box for the Instrument Path
        instrument_path_entry = ttk.Entry(
            self.instrumentFrame, textvariable=self.instrumentFrame_vars["instrument_path"])

        # Path File Explorer Button
        pathbutton = ttk.Button(
            self.instrumentFrame, text="File Explorer", command=lambda: self.setInstrumentPath())

        # ==========================================================
        # Grid Instrument Widgets
        # ==========================================================

        pathlabel.grid(column=0, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        instrument_path_entry.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        pathbutton.grid(column=2, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

    def setInstrumentPath(self):
        filename = fd.askopenfilename(title="Select Path", initialdir=os.path.dirname(
            os.path.abspath(__file__)), filetypes=(('VST3 Plugin', '.dll .vst3')))
        self.instrumentFrame_vars['instrument_path'].set(filename)

    def setEffectPath(self):
        effectfilename = fd.askopenfilename(title="Select Path", initialdir=os.path.dirname(
            os.path.abspath(__file__)), filetypes=(('VST3 Plugin', '.dll .vst3')))
        self.effectFrame_vars['effect_path'].set(effectfilename)

    def create_noteframe(self):
        # ==========================================================
        # Note Frame
        # ==========================================================

        self.noteFrame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Note")

        # ==========================================================
        # Note Variables
        # ==========================================================

        # Variables
        self.noteFrame_vars: Dict[str, tk.StringVar] = {
            "key_value": tk.StringVar(value="0"),
            "duration_value": tk.StringVar(value="0"),
            "velocity_value": tk.StringVar(value="0"),
            "frequency_value": tk.StringVar(value="0"),
        }

        # Variable trace callbacks

        for key in self.noteFrame_vars:
            self.noteFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_note_vals())

        # ==========================================================
        # Create Note Widgets
        # ==========================================================

        # Key Label
        key_Label = ttk.Label(
            self.noteFrame, text="Note Key")

        # Velocity Label
        velocity_Label = ttk.Label(
            self.noteFrame, text="Velocity / Strength")

        # Duration Label
        duration_Label = ttk.Label(
            self.noteFrame, text="Note Duration")

        # Frequency Label
        frequency_Label = ttk.Label(
            self.noteFrame, text="Note Frequency (Hz)")

        # Spinbox for note # and octave
        key_Spinbox = ttk.Spinbox(
            self.noteFrame, from_=0.0, to=127.0, textvariable=self.noteFrame_vars["key_value"], wrap=True)

        # Velocity Spinbox
        velocity_Spinbox = ttk.Spinbox(
            self.noteFrame, from_=0.0, to=127.0, textvariable=self.noteFrame_vars["velocity_value"], wrap=True)

        # Duration of Note Spinbox
        duration_Spinbox = ttk.Spinbox(
            self.noteFrame, from_=0.0, to=10000.0, textvariable=self.noteFrame_vars["duration_value"], increment=0.1, wrap=True)

        # Frequency of Note Spinbox
        frequency_Spinbox = ttk.Spinbox(
            self.noteFrame, from_=0.0, to=10000.0, textvariable=self.noteFrame_vars["frequency_value"], increment=0.1, wrap=True)

        # ==========================================================
        # Grid Note Widgets
        # ==========================================================

        key_Label.grid(column=1, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        key_Spinbox.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        velocity_Label.grid(column=1, row=2, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        velocity_Spinbox.grid(column=1, row=3, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        duration_Label.grid(column=1, row=4, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        duration_Spinbox.grid(column=1, row=5, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        frequency_Label.grid(column=1, row=6, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        frequency_Spinbox.grid(column=1, row=7, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

    def create_effectframe(self):
        # ==========================================================
        # Effect Frame
        # ==========================================================

        self.effectFrame = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="Effect")

        # Path File Explorer Button
        pathbutton = ttk.Button(
            self.effectFrame, text="File Explorer", command=lambda: self.setEffectPath())

        # ==========================================================
        # Instrument Variables
        # ==========================================================

        # Variables
        self.effectFrame_vars: Dict[str, tk.StringVar] = {
            "effect_path": tk.StringVar()
        }

        # Variable trace callbacks

        for key in self.effectFrame_vars:
            self.effectFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_effect_vals())

        # ==========================================================
        # Create Instrument Widgets
        # ==========================================================

        # Path Label
        pathlabel = ttk.Label(
            self.effectFrame, text="Effect Path", justify="center")

        # Entry box for the Instrument Path
        effect_path_entry = ttk.Entry(
            self.effectFrame, textvariable=self.effectFrame_vars["effect_path"])

        # Path File Explorer Button
        pathbutton = ttk.Button(
            self.effectFrame, text="File Explorer", command=lambda:  self.setEffectPath())

        # ==========================================================
        # Grid Instrument Widgets
        # ==========================================================

        pathlabel.grid(column=0, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        effect_path_entry.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
        pathbutton.grid(column=2, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)


# ==========================================================
# Adders
# ==========================================================


    def add_project(self):
        new_project_name = "Project %d" % (
            len(self.projects) + 1)

        self.tree.insert('', 'end', text=new_project_name, tags=["project"])

        # Add new project to project dict
        self.projects.update({new_project_name: Project(new_project_name)})
    # Creates an instrument under a project, With the values from

    def add_instrument(self):
        # If nothing is selected, return
        if not self.isTreeNodeSelected():
            return

        project_tkID = self.getValueTypeOfSelection("project")["tkID"]
        project_name = self.getValueTypeOfSelection("project")["name"]

        instrument_number = self.projects[project_name].getNumberOfInstruments(
        ) + 1
        instrument_name = "Instrument %d" % instrument_number

        new_instrument: Instrument = Instrument(instrument_name)

        self.tree.insert(project_tkID, 'end', text=instrument_name,
                         tags=["instrument"])

        self.projects[project_name].addInstrument(new_instrument)

    def add_effect(self):
        if not self.isTreeNodeSelected() or self.getValueTypeOfSelection("instrument") == None:
            return

        project_name = self.getValueTypeOfSelection("project")["name"]

        instrument_tkID = self.getValueTypeOfSelection("instrument")["tkID"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        instrument_class: Instrument = self.projects[project_name].getInstrument(
            instrument_name)

        effect_number = instrument_class.getEffectCount() + 1
        effect_name = "Effect %d" % effect_number
        effect = Effect(effect_name)

        self.tree.insert(instrument_tkID, 'end',
                         text=effect_name, tags=["effect"])

        instrument_class.add_effect(effect)

    def add_note(self):
        if not self.isTreeNodeSelected() or self.getValueTypeOfSelection("instrument") == None:
            return

        project_name = self.getValueTypeOfSelection("project")["name"]

        instrument_tkID = self.getValueTypeOfSelection("instrument")["tkID"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        instrument_class: Instrument = self.projects[project_name].getInstrument(
            instrument_name)

        note_number = instrument_class.getNoteCount() + 1
        note_name = "Note %d" % note_number
        note = Note(note_name)

        self.tree.insert(instrument_tkID, 'end', text=note_name, tags=["note"])

        instrument_class.add_note(note)


# ==========================================================
# Node Delete
# ==========================================================

    def selected_note_delete(self):
        if len(self.tree.selection()) == 0:
            return

        for selection in self.tree.selection():
            if self.tree.exists(selection):
                self.tree.delete(selection)

# ==========================================================
# Project Render
# ==========================================================

    def render(self):
        if not self.isTreeNodeSelected():
            return

        project_str = self.getValueTypeOfSelection("project")["name"]

        SoundGenerator.generate_project(
            self.projects[project_str], "eggs2.wav")

        scene = AnimRenderScene()
        scene.load_project(self.projects[project_str], "eggs2.wav")
        scene.render()

        messagebox.showinfo(title="Render Complete",
                            message="The render has been completed")


# ==========================================================
# Utility Functions
# ==========================================================

    # Checks what item is pressed in the selection tree and changes the middle frame accordingly


    def tree_select(self):
        if not self.isTreeNodeSelected():
            return

        sel_id = self.tree.selection()[0]

        type_tag = self.tree.item(sel_id)["tags"][0]

        # Show Edit Frame

        frame_dict: Dict[str, ttk.LabelFrame] = {
            "project": self.projectFrame,
            "instrument": self.instrumentFrame,
            "note": self.noteFrame,
            "effect": self.effectFrame
        }

        for frame_key in frame_dict:
            if frame_key == type_tag:
                frame_dict[frame_key].grid(column=1, row=0, sticky=(
                    tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)
            else:
                frame_dict[frame_key].grid_forget()

        # Load values from struct into frame
        if type_tag == "project":
            self.load_project_vals()
        elif type_tag == "instrument":
            self.load_instrument_vals()
        elif type_tag == "note":
            self.load_note_vals()
        elif type_tag == "effect":
            self.load_effect_vals()

    def isTreeNodeSelected(self) -> bool:
        return len(self.tree.selection()) != 0

    def getValueTypeOfSelection(self, parent_type: str) -> Dict[str, str]:
        current_selection = self.tree.selection()[0]

        while (parent_type not in self.tree.item(current_selection)["tags"]):
            if (self.tree.parent(current_selection)):
                current_selection = self.tree.parent(current_selection)
            else:
                return None

        final_dict = {
            "tkID": current_selection,
            "name": self.tree.item(current_selection)["text"]
        }

        return final_dict

    def load_project_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]

        project_class = self.projects[project_name]

        self.pause_var_trace()

        self.projectFrame_vars["sample_rate"].set(
            str(project_class.getSampleRate()))
        self.projectFrame_vars["runtime"].set(str(project_class.getRuntime()))

        self.resume_var_trace()

    def load_instrument_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)

        self.pause_var_trace()

        self.instrumentFrame_vars["instrument_path"].set(
            instrument_class.getInstrumentPath())

        self.resume_var_trace()

    def load_note_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        note_name = self.getValueTypeOfSelection("note")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)
        note_class = instrument_class.getNote(note_name)

        self.pause_var_trace()

        self.noteFrame_vars["key_value"].set(note_class.getKey())
        self.noteFrame_vars["duration_value"].set(note_class.getDuration())
        self.noteFrame_vars["velocity_value"].set(note_class.getVelocity())
        self.noteFrame_vars["frequency_value"].set(note_class.getFrequency())

        self.resume_var_trace()

    def load_effect_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        effect_name = self.getValueTypeOfSelection("effect")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)
        effect_class = instrument_class.getEffect(effect_name)

        self.pause_var_trace()

        self.effectFrame_vars["effect_path"].set(effect_class.getEffectPath())

        self.resume_var_trace()

    def update_project_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]

        project_class = self.projects[project_name]

        for value_key in self.projectFrame_vars:
            if self.projectFrame_vars[value_key].get() == "":
                return

        sample_rate = self.projectFrame_vars["sample_rate"].get()
        run_time = self.projectFrame_vars["runtime"].get()

        project_class.setSampleRate(int(sample_rate))
        project_class.setRuntime(float(run_time))

    def update_instrument_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)

        instrument_class.setInstrumentPath(
            self.instrumentFrame_vars["instrument_path"].get())

    def update_note_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        note_name = self.getValueTypeOfSelection("note")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)
        note_class = instrument_class.getNote(note_name)

        # Gets note values from spin
        for value_key in self.noteFrame_vars:
            if self.noteFrame_vars[value_key].get() == "":
                return

        key = self.noteFrame_vars["key_value"].get()
        duration = self.noteFrame_vars["duration_value"].get()
        velocity = self.noteFrame_vars["velocity_value"].get()
        frequency = self.noteFrame_vars["frequency_value"].get()

        note_class.setKey(int(key))
        note_class.setDuration(float(duration))
        note_class.setVelocity(int(velocity))
        note_class.setFrequency(float(frequency))

    def update_effect_vals(self):
        project_name = self.getValueTypeOfSelection("project")["name"]
        instrument_name = self.getValueTypeOfSelection("instrument")["name"]
        effect_name = self.getValueTypeOfSelection("effect")["name"]

        project_class = self.projects[project_name]
        instrument_class = project_class.getInstrument(instrument_name)
        effect_class = instrument_class.getEffect(effect_name)

        effect_class.setEffectPath(self.effectFrame_vars["effect_path"].get())

    def pause_var_trace(self):
        for key in self.projectFrame_vars:
            trace_info = self.projectFrame_vars[key].trace_info()[0]
            self.projectFrame_vars[key].trace_remove(
                trace_info[0], trace_info[1])

        for key in self.instrumentFrame_vars:
            trace_info = self.instrumentFrame_vars[key].trace_info()[0]
            self.instrumentFrame_vars[key].trace_remove(
                trace_info[0], trace_info[1])

        for key in self.noteFrame_vars:
            trace_info = self.noteFrame_vars[key].trace_info()[0]
            self.noteFrame_vars[key].trace_remove(trace_info[0], trace_info[1])

        for key in self.effectFrame_vars:
            trace_info = self.effectFrame_vars[key].trace_info()[0]
            self.effectFrame_vars[key].trace_remove(
                trace_info[0], trace_info[1])

    def resume_var_trace(self):
        for key in self.projectFrame_vars:
            self.projectFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_project_vals())

        for key in self.instrumentFrame_vars:
            self.instrumentFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_instrument_vals())

        for key in self.noteFrame_vars:
            self.noteFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_note_vals())

        for key in self.effectFrame_vars:
            self.effectFrame_vars[key].trace(
                "w", lambda x, y, z: self.update_effect_vals())
