from plugwndw import *
from time import time
from tkinter import filedialog, messagebox
from pedalboard import Pedalboard
from pedalboard.io import AudioFile

SAMPLE_RATE = 44100.0
FX_LIST = ["Bitcrush", "Chorus", "Clipping", "Compressor", "Delay", "Gain", "Limiter",  "Phaser", "Reverb"]

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
        self.fx_currentbox.bind("<Button-3>", self.show_plugin_window)
        self.fx_currentbox.pack()
        self.process_button = tk.Button(self.root, text="Process Audio", command=self.process)
        self.process_button.pack()
        self.selected_plugins = {}

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

    def show_plugin_window(self, event):
        selected_idx = self.fx_currentbox.curselection()
        if selected_idx:
            fx_name = self.fx_currentbox.get(selected_idx[0])
            plugin_window = PluginWindow(self.root, fx_name)
            self.root.wait_window(plugin_window.window)
            selected_parameters = plugin_window.get_parameters()
            self.selected_plugins[fx_name] = selected_parameters

    def get_fx_parameters(self, fx_name):
        parameters = {}
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel) and window.wm_title() == fx_name:
                for child in window.winfo_children():
                    if isinstance(child, RadialKnob):
                        parameters[child.cget("label")] = child.get()
        return parameters

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
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    pass
