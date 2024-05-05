from rknob import *
from pedalboard import Bitcrush, Chorus, Clipping, Compressor, Delay, Gain, Limiter, Phaser, Reverb
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
    
if __name__ == "__main__":
    pass