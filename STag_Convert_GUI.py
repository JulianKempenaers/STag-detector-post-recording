import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import ast
import os

SETTINGS_FILE = "recent_convert_settings.txt"
DEFAULT_SETTINGS = {
    "stag_libraries": [17, 19, 21, 23],
    "filename_addon": "",
    "frame_reconstruction": False,
    "n_cols": 21,
    "display_recentID_bar": True
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                contents = f.read()
                return ast.literal_eval(contents)
        except Exception as e:
            print("Error loading settings:", e)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        f.write(str(settings))

class STag_Convert_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Convert raw data (.npz) to videos (.mp4) and optionally detect tags")

        self.settings = load_settings()
        self.stag_vars = {}
        self.vars = {}

        self.style=ttk.Style()
        self.default_label_fg = self.style.lookup("TLabel", "foreground")
        

        self.create_widgets()
        self.started = False

        

    def create_widgets(self):
        ttk.Label(self.root, text="Convert raw data (.npz) to videos (.mp4) and optionally detect tags", font=("TkDefaultFont", 16, "bold")).grid(row=0, column=0, pady=(10, 5))
        frame = ttk.LabelFrame(self.root, text="Settings")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        #---------------------- frame_reconstruction (checkbox)-------------------
        ttk.Label(frame, text="Frame Reconstruction:", font=("TkDefaultFont", 13, "bold")).grid(row=1, column=0, sticky="w", pady=(10, 10), padx=10)
        ttk.Label(frame, text="On: your .mp4 videos will look like a normal video\nOff:Only pixels with detected movement will be displayed in the video, and the background will be black. \nNote: reconstruction takes longer because each frame is overlayed onto the key frame, \nand the entire key frame gets scanned for tags", font=("TkDefaultFont", 10)).grid(row=2, column=0, sticky="w", pady=(10,0), padx=10)
        self.vars["frame_reconstruction"] = ttk.BooleanVar(value=self.settings.get("frame_reconstruction", False))
        ttk.Checkbutton(frame, text="Frame Reconstruction", variable=self.vars["frame_reconstruction"], bootstyle="success,round-toggle").grid(row=3, column=0, sticky="w", pady=1, padx=10)

        # -------------------filename_addon (text entry)----------------------------
        ttk.Label(frame, text= "Filename Add-on (Optional)", font=("TkDefaultFont", 13, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(frame, text="This will be added to the end of the filename of your saved .mp4 video.", font=("TkDefaultFont", 10)).grid(row=5,column=0,sticky="w", padx=10)
        self.vars["filename_addon"] = ttk.StringVar(value=self.settings.get("filename_addon", ""))
        ttk.Entry(frame, textvariable=self.vars["filename_addon"], bootstyle="success").grid(row=6, column=0, sticky="w", padx=10, pady=2)

        # --------------------STag libraries (checkboxes)------------------------------
        ttk.Label(frame, text="Stag Libraries (Optional):", font=("TkDefaultFont", 13, "bold")).grid(row=1, column=1, sticky="w", pady=(10,0))
        ttk.Label(frame, text="Which tag libraries (if any) would you like to detect? \nNote: If no libraries are selected, your .npz files will still be converted to .mp4.", font=("TkDefaultFont", 10)).grid(row=2, column=1, sticky="w")
        stag_frame = ttk.Frame(frame)
        stag_frame.grid(row=3, column=1, sticky="w", pady=2)
        for i, val in enumerate([11, 13, 15, 17, 19, 21, 23]):
            var = ttk.BooleanVar(value=val in self.settings["stag_libraries"])
            self.stag_vars[val] = var
            ttk.Checkbutton(stag_frame, text=str(val), variable=var, bootstyle="success,round-toggle").grid(row=i, column=1, sticky="w", padx=10)  

        # -----------------------------n_cols (spinbox)--------------------------
        self.n_cols_title=ttk.Label(frame, text="Tag memory", font=("TkDefaultFont", 13, "bold"))
        self.n_cols_title.grid(row=4, column=1, sticky="w", padx=10, pady=(10, 0))
        self.n_cols_lable=ttk.Label(frame, text="Tag Memory = 1: Tags are not remembered across frames and they will not be colour coded. \nTag Memory >1: This number of tags will be remembered across frames and they will be colour coded. \nNote: If Tag Memory is set higher than 1, and if more than this number of tags appear within a single frame, the code WILL CRASH. \nNote: If no STag Libraries are selected, the code ignores this input. ", font=("TkDefaultFont", 10))
        self.n_cols_lable.grid(row=5, column=1, sticky="w", padx=10, pady=(10, 0))
        self.vars["n_cols"] = ttk.IntVar(value=self.settings.get("n_cols", 21))
        self.n_cols_spinbox=ttk.Spinbox(frame, from_=1, to=21, textvariable=self.vars["n_cols"], bootstyle="success", width=5)
        self.n_cols_spinbox.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        # ----------------------display_recentID_Bbar? (checkbox)------------------------------
        self.recentID_bar_title=ttk.Label(frame, text= "Recent ID Bar", font=("TkDefaultFont", 13, "bold"))
        self.recentID_bar_title.grid(row=7, column=1, sticky="w", padx=10, pady=(10,0))
        self.recentID_bar_lable=ttk.Label(frame, text= "On: Underneath the video, a bar is added to display the numbers of most recently detected IDs and their colour. \nOff: No bar is added underneath the video. \nNote: when Tag Memory = 1, or when no STag libraries are selected, the code ignores this input and there will not be a bar.", font=("TkDefaultFont", 10))
        self.recentID_bar_lable.grid(row=8, column=1, sticky="w", padx=10, pady=(10,0))
        self.vars["display_recentID_bar"] = ttk.BooleanVar(value=self.settings.get("display_recentID_bar", True))
        self.recentID_bar=ttk.Checkbutton(frame, text="display recentID bar?", variable=self.vars["display_recentID_bar"], bootstyle="success,round-toggle")
        self.recentID_bar.grid(row=9, column=1, sticky="w", pady=2, padx=10)


        # Function to enable/disable n_cols & recentID bar based on STag selection
        def update_n_cols_state():
            if not any(var.get() for var in self.stag_vars.values()):
                self.n_cols_spinbox.state(["disabled"])
                self.n_cols_title.configure(foreground="grey")
                self.n_cols_lable.configure(foreground="grey")
                self.recentID_bar.state(["disabled"])
                self.recentID_bar_title.configure(foreground="grey")
                self.recentID_bar_lable.configure(foreground="grey")
            else:
                self.n_cols_spinbox.state(["!disabled"])
                self.n_cols_title.configure(foreground=self.default_label_fg)
                self.n_cols_lable.configure(foreground=self.default_label_fg)
                self.recentID_bar.state(["!disabled"])
                self.recentID_bar_title.configure(foreground=self.default_label_fg)
                self.recentID_bar_lable.configure(foreground=self.default_label_fg)


        for var in self.stag_vars.values():
            var.trace_add("write", lambda *args: update_n_cols_state())
        update_n_cols_state()

        # --------------------------------Start button-----------------------------------
        start_btn = ttk.Button(self.root, text="START", command=self.on_start, bootstyle="danger")
        start_btn.grid(pady=10)

    def on_start(self):
        try:
            settings = {
                "stag_libraries": [k for k, v in self.stag_vars.items() if v.get()],
                "filename_addon": self.vars["filename_addon"].get().strip(),
                "frame_reconstruction": self.vars["frame_reconstruction"].get(),
                "n_cols": int(self.vars["n_cols"].get()),
                "display_recentID_bar": self.vars["display_recentID_bar"].get()
            }
            save_settings(settings)
            self.started = True
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")

if __name__ == "__main__":
    root = ttk.Window(themename="solar")
    app = STag_Convert_GUI(root)
    root.mainloop()
