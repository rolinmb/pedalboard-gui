import tkinter as tk
import math

class RadialKnob(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width=100, height=100, bg='white')
        self.value = 0
        self.center = 50, 50
        self.radius = 40
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        
        self.draw_knob()
    
    def draw_knob(self):
        self.delete("knob")
        x0, y0 = self.center
        angle = math.radians(self.value * 270 / 100 + 135)
        x1 = x0 + self.radius * math.cos(angle)
        y1 = y0 + self.radius * math.sin(angle)
        self.create_oval(x0-self.radius, y0-self.radius, x0+self.radius, y0+self.radius, outline='black', width=2)
        self.create_line(x0, y0, x1, y1, fill='red', width=2, tags="knob")
    
    def on_click(self, event):
        self.update_value(event.x, event.y)
    
    def on_drag(self, event):
        self.update_value(event.x, event.y)
    
    def update_value(self, x, y):
        x0, y0 = self.center
        angle = math.atan2(y-y0, x-x0)
        self.value = int((math.degrees(angle) - 135) * 100 / 270)
        if self.value < 0:
            self.value = 0
        elif self.value > 100:
            self.value = 100
        self.draw_knob()
