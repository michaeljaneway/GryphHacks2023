import tkinter as tk
from tkinter import ttk
import sv_ttk
import pathlib


class MainApplication(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title("The Sounds of the Future")

        # https://github.com/rdbende/Sun-Valley-ttk-theme

        # All of these previous lines of code are essentially setting up the frame and window, and how they dynamically resize
        self.frameleft = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameLEFT")
        self.frameleft.grid(column=0, row=0, sticky=(
            tk.N, tk.S, tk.W, tk.E), padx=15, pady=15)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # p = ttk.Progressbar(self.frameleft, orient=tk.HORIZONTAL, length=200, mode='determinate')
        # p.grid(column=0,row=1,sticky=(tk.W,tk.E),padx=20,pady=20)
        # p.start()
        sv_ttk.use_dark_theme()
        note_count = 1
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

        self.framemid = ttk.LabelFrame(
            self, padding="20", width=150, height=200, text="FrameMID")
        self.framemid.grid(column=1, row=0, sticky=(
            tk.N, tk.E, tk.S, tk.W), padx=15, pady=15)

        self.spinval = tk.StringVar(value="0")
        self.keyselector = ttk.Spinbox(
            self.framemid, from_=0.0, to=127.0, textvariable=self.spinval)
        self.keyselector.grid(column=1, row=1, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        self.spinval.trace("w", lambda x, y, z: self.show_key())

        self.keyselector_text = ttk.Label(
            self.framemid, text="Note Key", justify="center")
        self.keyselector_text.grid(column=1, row=0)

        self.Add_Note_button = ttk.Button(
            self.frameleft, text="Add Note", command=lambda: self.add_note()
        )
        self.Add_Note_button.grid(column=2, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        delete_button = ttk.Button(
            self.frameleft, text="Delete Note", command=lambda: self.delete_note())
        delete_button.grid(column=0, row=0, sticky=(
            tk.E, tk.W), padx=10, pady=10)

        render_button = ttk.Button(
            self.framemid, text="Render Audio", command=lambda: self.render())
        render_button.grid(column=0, row=3, sticky=(
            tk.E, tk.W), padx=50, pady=66)

        self.velocityval = tk.StringVar(value="0")
        self.velocitybox = ttk.Spinbox(
            self.framemid, from_=0.0, to=127.0, textvariable=self.velocityval)
        self.velocitybox.grid(column=1, row=3, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)

        self.velocitybox_text = tk.Label(
            self.framemid, text="Velocity", justify="center")
        self.velocitybox_text.grid(column=1, row=2)

        # tk.Text.insert()
    def add_note(self):
        self.instrument_tree.insert('Instr1', 'end', text=number_to_note(int(self.spinval.get())))
        self.note_count += 1

    def delete_note(self):
        self.instrument_tree.delete('Instr1')

    def funny_function(self):
        print("Helloeggs")

    def render(self):
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
