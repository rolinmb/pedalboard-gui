from rknob import RadialKnob
from time import time
import tkinter as tk
from tkinter import filedialog, messagebox
from pedalboard import Pedalboard, Bitcrush, Chorus, Clipping, Compressor, Delay, Gain, Limiter, Phaser, Reverb
from pedalboard.io import AudioFile
"""
tkinter_version = tk.Tcl().eval("info patchlevel")
print("\napp.py tkinter version: "+tkinter_version+"\n")
tk._test()
"""
# Pedalboard built-in FX class member vars and init / default values
#print(vars(Bitcrush)) # bit_depth = 8 (float >= 32.0 && float <= 0.0)
#print(vars(Chorus)) # rate_hz = 1.0 (float <= 100.0 && float >= 0.0), depth = 0.25 (float), centre_delay_ms = 7.0 (float), feedback = 0.0 (float), mix = 0.5 (float <= 1.0 && float >= 0.0)
#print(vars(Clipping)) # threshold_db = -6.0 (float)
#print(vars(Compressor)) # threshold_db = 0 (float), ratio = 1 (float >= 1.0), attack_ms = 1.0 (float), release_ms = 100 (float)
#print(vars(Delay)) # delay_seconds = 0.5 (float >= 0.0), feedback = 0.0 (float <= 1.0 && float >= 0.0) , mix = 0.5 (float <= 1.0 && float >= 0.0)
#print(vars(Gain)) # gain_db = 1.0 (float)
#print(vars(Limiter)) # threshold_db = -10.0 (float), release_ms = 100.0 (float)
#print(vars(Phaser)) # rate_hz = 1.0 (float >= 0.0), depth = 0.5 (float >= 0.0), centre_frequency_hz = 1300.0 (float >= 0.0), feedback = 0.0 (float <= 1.0 && float >= 0.0), mix = 0.5 (float <= 1.0 && float >= 0.0)
#print(vars(Reverb)) # room_size = 0.5, damping = 0.5, wet_level = 0.33, dry_level = 0.4, width = 1.0, freeze_mode = 0.0 (all float <= 1.0 && float >= 0.0)

SAMPLE_RATE = 44100.0
FX_LIST = ["Bitcrush", "Chorus", "Clipping", "Compressor", "Delay", "Gain", "Limiter",  "Phaser", "Reverb"]
FX_DICT = {
    "Bitcrush": Bitcrush,
    "Chorus": Chorus,
    "Clipping": Clipping,
    "Compressor": Compressor,
    "Delay": Delay,
    "Gain": Gain,
    "Limiter": Limiter,
    "Phaser": Phaser,
    "Reverb": Reverb
}
PARAMNAMESMAP = {
    "Bitcrush": ["bit_depth"],
    "Chorus": ["rate_hz", "depth", "centre_delay_ms", "feedback", "mix"],
    "Clipping": ["threshold_db"],
    "Compressor": ["threshold_db", "ratio", "attack_ms", "release_ms"],
    "Delay": ["delay_seconds", "feedback", "mix"],
    "Gain": ["gain_db"],
    "Limiter": ["threshold_db", "release_ms"],
    "Phaser": ["rate_hz", "depth", "centre_frequency_hz", "feedback", "mix"],
    "Reverb": ["room_size", "damping", "wet_level", "dry_level", "width", "freeze_mode"]
}

class PluginWindow:
    def __init__(self, root, plugin_name):
        self.root = root
        self.fx_name = plugin_name
        self.parameters = self.get_fx_parameter_names()
        self.knobs = []
        self.create_window()

    def get_fx_parameter_names(self):
        return PARAMNAMESMAP.get(self.fx_name, [])
    
    def create_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title(self.fx_name)
        for param_name in self.parameter_names:
            if hasattr(FX_DICT[self.fx_name], param_name):
                param_value = getattr(FX_DICT[self.fx_name], param_name)
                if isinstance(param_value, float):
                    initial_value = getattr(FX_DICT[self.fx_name], param_name)
                    knob = RadialKnob(self.window, label=param_name, from_=0, to=1, resolution=0.01, initial_value=initial_value)
                    knob.pack()
                    self.knobs.append(knob)

    def get_parameters(self):
        parameters = {}
        for knob, param_name in zip(self.knobs, self.parameter_names):
            parameters[param_name] = knob.get()
        return parameters

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selection")
        self.input_file_path = None
        self.file_open_button = tk.Button(self.root, text="Open File", command=self.open_file_dialog)
        self.file_open_button.pack(pady=20)
        self.selected_file_label = tk.Label(self.root, text="Selected File: None")
        self.selected_file_label.pack()
        self.output_file_path = None
        self.output_file_label = tk.Label(self.root, text="Output Filename:")
        self.output_file_label.pack()
        self.output_file_entry = tk.Entry(self.root)
        self.output_file_entry.pack()
        self.output_file_entry.bind("<Leave>", self.check_output_entry)
        self.board = None
        self.effects = []
        self.fx_selectbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.fx_selectbox.pack()
        for effect in FX_LIST:
            self.fx_selectbox.insert(tk.END, effect)
        self.add_fx_button = tk.Button(self.root, text="Add Effect", command=self.add_fx)
        self.add_fx_button.pack()
        self.remove_fx_button = tk.Button(self.root, text="Remove Effect", command=self.remove_fx)
        self.remove_fx_button.pack()
        self.fx_currentbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.fx_currentbox.pack()
        self.process_button = tk.Button(self.root, text="Process Audio", command=self.process)
        self.process_button.pack()

    def open_file_dialog(self):
        self.input_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if self.input_file_path:
            self.selected_file_label.config(text=f"Selected File:\n{self.input_file_path}")

    def check_output_entry(self, event):
        fout = self.output_file_entry.get()
        if fout:
            if len(fout) < 5 or fout[-4:] != ".wav":
                messagebox.showerror("Make sure the output filename ends with .wav")
            self.output_file_path = fout
            self.output_file_label.config(text=f"Output Filename:\n{self.output_file_path}")
        else:
            self.output_file_path = None

    def add_fx(self):
        selected_index = self.fx_selectbox.curselection()
        if selected_index:
            new_effect = FX_LIST[int(selected_index[0])]
            self.effects.append(new_effect)
            self.fx_currentbox.insert(tk.END, new_effect)
        else:
            messagebox.showerror("Error", "Please select an effect to add")

    def remove_fx(self):
        selected_index = self.fx_currentbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            removed_effect = self.effects.pop(selected_index)
            self.fx_currentbox.delete(selected_index)
        else:
            messagebox.showerror("Error", "Please select an effect to remove")

    def process(self):
        start = time()
        if self.input_file_path and self.output_file_path:
            with AudioFile(self.input_file_path).resampled_to(SAMPLE_RATE) as wav:
                audio = wav.read(wav.frames)
            toApply = []
            for fx_name in self.effects:
                if fx_name in FX_LIST:
                    fx_plugin = FX_DICT[fx_name]
                    fx_params = self.get_fx_parameters(fx_name)
                    toApply.append(fx_plugin(**fx_params))
            self.board = Pedalboard(toApply)
            effected = self.board(audio, SAMPLE_RATE)
            with AudioFile(self.output_file_path, "w", SAMPLE_RATE, effected.shape[0]) as fout:
                fout.write(effected)
        else:
            if self.input_file_path and not self.output_file_path:
                messagebox.showerror("Error", "Please enter an output file name")
            elif self.output_file_path and not self.input_file_path:
                messagebox.showerror("Error", "Please select an input .wav file")
            else:
                messagebox.showerror("Error", "Please select an input .wav and enter an output .wav")
        print(f"app.py process() Execution Time: {str(round(time() - start, 2))} seconds")

    def get_fx_parameters(self, fx_name):
        parameters = {}
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel) and window.wm_title() == fx_name:
                for child in window.winfo_children():
                    if isinstance(child, RadialKnob):
                        parameters[child.cget("label")] = child.get()
        return parameters

    def show_plugin_window(self, event):
        selected_idx = self.fx_currentbox.curselection()
        if selected_idx:
            fx_name = self.fx_currentbox.get(selected_idx[0])
            PluginWindow(self.root, fx_name)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    pass
