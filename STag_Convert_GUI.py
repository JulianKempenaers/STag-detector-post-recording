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
        self.root.title("STag Convert Settings")

        self.settings = load_settings()
        self.stag_vars = {}
        self.vars = {}

        self.create_widgets()
        self.started = False

    def create_widgets(self):
        frame = ttk.LabelFrame(self.root, text="Settings")
        frame.grid(padx=10, pady=10)

        # STag libraries (checkboxes)
        ttk.Label(frame, text="stag_libraries: Select which STAG tag libraries to detect.").grid(row=0, column=0, sticky="w")
        stag_frame = ttk.Frame(frame)
        stag_frame.grid(row=1, column=0, sticky="w", pady=2)
        for i, val in enumerate([17, 19, 21, 23]):
            var = ttk.BooleanVar(value=val in self.settings["stag_libraries"])
            self.stag_vars[val] = var
            ttk.Checkbutton(stag_frame, text=str(val), variable=var, bootstyle="success,round-toggle").grid(row=i, column=0, sticky="w")

        # filename_addon (text entry)
        ttk.Label(frame, text="filename_addon: Optional. This will be added to the filename of your saved video. Leave blank if not needed.").grid(row=0, column=1, sticky="w", padx=10)
        self.vars["filename_addon"] = ttk.StringVar(value=self.settings.get("filename_addon", ""))
        ttk.Entry(frame, textvariable=self.vars["filename_addon"], bootstyle="success").grid(row=1, column=1, sticky="w", padx=10, pady=2)

        # frame_reconstruction (checkbox)
        ttk.Label(frame, text="frame_reconstruction: Choose whether to run STAG detection on full frames or sparse frames.\nFull reconstruction takes longer. Sparse frames only save changed pixels.").grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.vars["frame_reconstruction"] = ttk.BooleanVar(value=self.settings.get("frame_reconstruction", False))
        ttk.Checkbutton(frame, text="Frame Reconstruction", variable=self.vars["frame_reconstruction"], bootstyle="success,round-toggle").grid(row=3, column=1, sticky="w", pady=2)

        # n_cols (spinbox)
        ttk.Label(frame, text="Track how many recent tags?\nControls how many recently detected tags are tracked and color-coded. If set to 1: tags are not tracked and no color coding will occur.").grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.vars["n_cols"] = ttk.IntVar(value=self.settings.get("n_cols", 21))
        ttk.Spinbox(frame, from_=1, to=21, textvariable=self.vars["n_cols"], bootstyle="success", width=5).grid(row=3, column=0, sticky="w", padx=10, pady=2)

        # display_recentID_Bbar? (checkbox)
        ttk.Label(frame, text= "Would you like to add a bar below the frame that displays \na list of the most recently detected IDs and their colour?").grid(row=4, column=0, sticky="w", padx=10, pady=(10,0))
        self.vars["display_recentID_bar"] = ttk.BooleanVar(value=self.settings.get("display_recentID_bar", True))
        ttk.Checkbutton(frame, text="display recentID bar?", variable=self.vars["display_recentID_bar"], bootstyle="success,round-toggle").grid(row=5, column=0, sticky="w", pady=2)

        # Start button
        start_btn = ttk.Button(self.root, text="Start", command=self.on_start, bootstyle="danger")
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
