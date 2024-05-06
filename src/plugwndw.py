from rknob import *
from pedalboard import Bitcrush, Chorus, Clipping, Compressor, Delay, Gain, Limiter, Phaser, Reverb
# Pedalboard built-in FX class member vars and init / default values
#print(vars(Bitcrush))
#print(vars(Chorus))
#print(vars(Clipping))
#print(vars(Compressor))
#print(vars(Delay))
#print(vars(Gain))
#print(vars(Limiter))
#print(vars(Phaser))
#print(vars(Reverb))

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

PARAMRANGES = {
    "Bitcrush": {"bit_depth": (0, 32.0)},  # Range from 0 to 32.0 for bit_depth
    "Chorus": {"rate_hz": (0, 100.0), "depth": (0, 1.0), "centre_delay_ms": (0, float('inf')), "feedback": (0, 1.0), "mix": (0, 1.0)},
    "Clipping": {"threshold_db": (float('-inf'), 0)},  # Range from negative infinity to 0 for threshold_db
    "Compressor": {"threshold_db": (0, float('inf')), "ratio": (1.0, float('inf')), "attack_ms": (0, float('inf')), "release_ms": (0, float('inf'))},
    "Delay": {"delay_seconds": (0, float('inf')), "feedback": (0, 1.0), "mix": (0, 1.0)},
    "Gain": {"gain_db": (float('-inf'), float('inf'))},  # Range from negative infinity to positive infinity for gain_db
    "Limiter": {"threshold_db": (float('-inf'), 0), "release_ms": (0, float('inf'))},
    "Phaser": {"rate_hz": (0, float('inf')), "depth": (0, 1.0), "centre_frequency_hz": (0, float('inf')), "feedback": (0, 1.0), "mix": (0, 1.0)},
    "Reverb": {"room_size": (0, 1.0), "damping": (0, 1.0), "wet_level": (0, 1.0), "dry_level": (0, 1.0), "width": (0, 1.0), "freeze_mode": (0, 1.0)}
}

class BaseEffectUI(tk.Frame):
    def __init__(self, master, effect_name):
        super().__init__(master)
        self.effect_name = effect_name
        self.parameters = PARAMNAMESMAP.get(self.effect_name, [])
        self.create_widgets()

    def create_widgets(self):
        for param_name in self.parameters:
            if hasattr(FX_DICT[self.effect_name], param_name):
                #param_range = PARAMRANGES.get(self.effect_name, {}).get(param_name, (0, 1))
                #initial_value = getattr(FX_DICT[self.effect_name], param_name)
                #knob = RadialKnob(self, label=param_name, from_=param_range[0], to=param_range[1], resolution=0.01, initial_value=initial_value)
                knob = RadialKnob(self)
                knob.pack()

    def get_parameters(self):
        parameters = {}
        for param_name in self.parameters:
            knob = self.nametowidget(param_name)
            parameters[param_name] = knob.get()
        return parameters

class BitcrushUI(BaseEffectUI):
    pass

class ChorusUI(BaseEffectUI):
    pass

class ClippingUI(BaseEffectUI):
    pass

class CompressorUI(BaseEffectUI):
    pass

class DelayUI(BaseEffectUI):
    pass

class GainUI(BaseEffectUI):
    pass

class LimiterUI(BaseEffectUI):
    pass

class PhaserUI(BaseEffectUI):
    pass

class ReverbUI(BaseEffectUI):
    pass

def create_effect_ui(master, effect_name):
    if effect_name in FX_DICT:
        return globals()[effect_name + "UI"](master, effect_name)
    else:
        print("Error occurred in plugwndw.py :: create_effect_ui")
        return None

"""
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
"""
class PluginWindow:
    def __init__(self, root, plugin_name):
        self.root = root
        self.fx_name = plugin_name
        self.ui = create_effect_ui(root, plugin_name)
        if self.ui:
            self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title(self.fx_name)
        self.ui.pack(in_=self.window)

    def get_parameters(self):
        if self.ui:
            return self.ui.get_parameters()
        else:
            return {}

if __name__ == "__main__":
    pass