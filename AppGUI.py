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
            self, padding="20", width=150, height=200, text="FrameLEFT")
        self.frameleft.grid(column=0, row=0, sticky=(
            tk.N, tk.S,tk.W), padx=15, pady=15)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # p = ttk.Progressbar(self.frameleft, orient=tk.HORIZONTAL, length=200, mode='determinate')
        # p.grid(column=0,row=1,sticky=(tk.W,tk.E),padx=20,pady=20)
        # p.start()

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
        self.instrument_tree.tag_configure('swag', background='green')
        self.instrument_tree.tag_bind('swag',"<1>", self.instrument_tree.focus())

        self.instrument_tree.bind(
            "<<TreeviewSelect>>", lambda event: self.tree_select())
        
        self.frameright = ttk.LabelFrame(self, padding="20", width=150, height=200, text="FrameRIGHT")
        self.frameright.grid(column=2, row=0, sticky=(
            tk.N, tk.S,tk.E), padx=15, pady=15)

        funny_button = ttk.Button(
            self.frameleft, text="Open Image", command=lambda: self.instrument_tree.grid_forget())
        funny_button.grid(column=0, row=0, sticky=(
            tk.N, tk.W, tk.E, tk.S), padx=20, pady=20)
        open_editor_button = ttk.Button(
            self.frameleft, text="Open Editor"
        )

        render_button = ttk.Button(
            self.frameleft, text="RENDER", command=lambda: self.render())
        render_button.grid(column=1, row=1, sticky=(
            tk.E, tk.W), padx=50, pady=66)

    def funny_function(self):
        print("Helloeggs")

    def render(self):
        print("renderrenderrender")

    def tree_select(self):
        print("Selected_obj")
