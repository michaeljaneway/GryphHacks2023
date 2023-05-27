import tkinter as tk
from tkinter import ttk
import sv_ttk


class MainApplication(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title("The Sounds of the Future")

        # https://github.com/rdbende/Sun-Valley-ttk-theme

        # All of these previous lines of code are essentially setting up the frame and window, and how they dynamically resize

        self.frameleft = ttk.LabelFrame(
            self, padding="20", width=200, height=200, text="Frame2")
        self.frameleft.grid(column=0, row=0, sticky=(
            tk.N, tk.S), padx=25, pady=25)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        sv_ttk.use_dark_theme()

        self.instrument_tree = ttk.Treeview(
            self)
        self.instrument_tree.grid(column=1, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)

        self.instrument_tree.insert('', 'end', 'Instr1', text="Instrument 1")
        self.instrument_tree.insert('Instr1', 'end', text="Note 1")
        self.instrument_tree.insert('Instr1', 'end', text="Note 2")
        self.instrument_tree.insert('Instr1', 'end', text="Effect 1")
        self.instrument_tree.insert('Instr1', 'end', text="Effect 2")
        self.instrument_tree.insert('', 'end', text='swag', tags=('swag'))

        self.instrument_tree.bind(
            "<<TreeviewSelect>>", lambda event: self.tree_select())

        funny_button = ttk.Button(
            self.frameleft, text="Open Image", command=lambda: self.instrument_tree.grid_forget())
        funny_button.grid(column=0, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=50, pady=100.2)
        open_editor_button = ttk.Button(
            self.frameleft, text="Open Editor"
        )

        render_button = ttk.Button(
            self.frameleft, text="RENDER", command=lambda: self.render())
        render_button.grid(column=1, row=1, sticky=(
            tk.E, tk.W), padx=50, pady=66.5)

    def funny_function(self):
        print("Helloeggs")

    def render(self):
        print("renderrenderrender")

    def tree_select(self):
        print("Selected_obj")
