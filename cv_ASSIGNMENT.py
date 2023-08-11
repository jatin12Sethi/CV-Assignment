#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import Image, ImageTk
from scipy.interpolate import CubicSpline

class WeavePatternGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weave Pattern Generator")

        self.canvas = tk.Canvas(self.root, width=500, height=400)
        self.canvas.pack()

        self.generate_button = ttk.Button(self.root, text="Generate Pattern", command=self.generate_pattern)
        self.generate_button.pack()

        self.num_horizontal_threads = tk.IntVar(value=10)
        self.num_vertical_threads = tk.IntVar(value=5)
        self.thread_thickness = tk.IntVar(value=20)
        self.thread_shape = tk.StringVar(value="cubic_spline")
        self.layout = tk.StringVar(value="simple")
        self.thread_color = tk.StringVar(value="#000000")
        self.background_color = tk.StringVar(value="#FFFFFF")

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Number of Horizontal Threads").pack()
        self.horizontal_threads_slider = ttk.Scale(self.root, from_=1, to=50, variable=self.num_horizontal_threads, orient="horizontal", command=self.update_sliders)
        self.horizontal_threads_slider.pack()

        self.horizontal_threads_label = ttk.Label(self.root, text=str(self.num_horizontal_threads.get()))
        self.horizontal_threads_label.pack()

        ttk.Label(self.root, text="Number of Vertical Threads").pack()
        self.vertical_threads_slider = ttk.Scale(self.root, from_=1, to=50, variable=self.num_vertical_threads, orient="horizontal", command=self.update_sliders)
        self.vertical_threads_slider.pack()

        self.vertical_threads_label = ttk.Label(self.root, text=str(self.num_vertical_threads.get()))
        self.vertical_threads_label.pack()

        ttk.Label(self.root, text="Thread Thickness").pack()
        self.thread_thickness_slider = ttk.Scale(self.root, from_=1, to=50, variable=self.thread_thickness, orient="horizontal", command=self.update_sliders)
        self.thread_thickness_slider.pack()

        self.thread_thickness_label = ttk.Label(self.root, text=str(self.thread_thickness.get()))
        self.thread_thickness_label.pack()

        ttk.Label(self.root, text="Thread Shape").pack()
        ttk.Combobox(self.root, values=["straight", "cubic_spline"], textvariable=self.thread_shape).pack()

        ttk.Label(self.root, text="Layout").pack()
        ttk.Combobox(self.root, values=["simple", "cubic_spline"], textvariable=self.layout).pack()

        thread_color_button = ttk.Button(self.root, text="Select Thread Color", command=self.select_thread_color)
        thread_color_button.pack()

        self.thread_color_label = ttk.Label(self.root, text="Thread Color: " + self.thread_color.get(), foreground=self.thread_color.get())
        self.thread_color_label.pack()

        background_color_button = ttk.Button(self.root, text="Select Background Color", command=self.select_background_color)
        background_color_button.pack()

        self.background_color_label = ttk.Label(self.root, text="Background Color: " + self.background_color.get(), foreground=self.background_color.get())
        self.background_color_label.pack()

#     def select_thread_color(self):
#         color = colorchooser.askcolor(title="Select Thread Color", color=self.thread_color.get())[1]
#         if color:
#             self.thread_color.set(color)

#     def select_background_color(self):
#         color = colorchooser.askcolor(title="Select Background Color", color=self.background_color.get())[1]
#         if color:
#             self.background_color.set(color)
            
    def update_sliders(self, *args):
        self.horizontal_threads_label.config(text=str(self.num_horizontal_threads.get()))
        self.vertical_threads_label.config(text=str(self.num_vertical_threads.get()))
        self.thread_thickness_label.config(text=str(self.thread_thickness.get()))

    def select_thread_color(self):
        color = colorchooser.askcolor(title="Select Thread Color", color=self.thread_color.get())[1]
        if color:
            self.thread_color.set(color)
            self.thread_color_label.config(text="Thread Color: " + self.thread_color.get(), foreground=self.thread_color.get())

    def select_background_color(self):
        color = colorchooser.askcolor(title="Select Background Color", color=self.background_color.get())[1]
        if color:
            self.background_color.set(color)
            self.background_color_label.config(text="Background Color: " + self.background_color.get(), foreground=self.background_color.get())

    def generate_pattern(self):
        width = 500
        height = 400
        num_horizontal_threads = self.num_horizontal_threads.get()
        num_vertical_threads = self.num_vertical_threads.get()
        thread_thickness = self.thread_thickness.get()
        thread_shape = self.thread_shape.get()
        layout = self.layout.get()
        thread_color_str = self.thread_color.get()
        
        if thread_color_str.startswith("#") and len(thread_color_str) == 7:
            thread_color = tuple(int(thread_color_str[i:i+2], 16) for i in (1, 3, 5))
        else:
            thread_color = (0, 0, 0)  # Default to black if invalid format

        background_color_str = self.background_color.get()
        if background_color_str.startswith("#") and len(background_color_str) == 7:
            background_color = tuple(int(background_color_str[i:i+2], 16) for i in (1, 3, 5))
        else:
            background_color = (255, 255, 255)  # Default to white if invalid format

        canvas = np.ones((height, width, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)

        if layout == "simple":
            for h in range(1, num_horizontal_threads):
                y = h * (height - 1) // num_horizontal_threads
                cv2.line(canvas, (0, y), (width, y), thread_color, thread_thickness)
            
            for v in range(1, num_vertical_threads):
                x = v * (width - 1) // num_vertical_threads
                cv2.line(canvas, (x, 0), (x, height), thread_color, thread_thickness)
    
        elif layout == "cubic_spline":
            # Generate horizontal threads using cubic spline
            for h in range(1, num_horizontal_threads):
                y = h * (height - 1) // num_horizontal_threads
                x_points = np.linspace(0, width, num_horizontal_threads)
                y_points = np.repeat(y, num_horizontal_threads)
                spline = CubicSpline(x_points, y_points)
                t = np.linspace(0, 1, num_horizontal_threads * 10)
                thread_points = np.column_stack((spline(t), np.repeat(y, t.size)))
                for i in range(thread_points.shape[0] - 1):
                    cv2.line(canvas, tuple(thread_points[i]), tuple(thread_points[i + 1]), thread_color, thread_thickness)
            
            # Generate vertical threads using cubic spline
            for v in range(1, num_vertical_threads):
                x = v * (width - 1) // num_vertical_threads
                y_points = np.linspace(0, height, num_vertical_threads)
                x_points = np.repeat(x, num_vertical_threads)
                spline = CubicSpline(y_points, x_points)
                t = np.linspace(0, 1, num_vertical_threads * 10)
                thread_points = np.column_stack((np.repeat(x, t.size), spline(t)))
                for i in range(thread_points.shape[0] - 1):
                    cv2.line(canvas, tuple(thread_points[i]), tuple(thread_points[i + 1]), thread_color, thread_thickness)

        img = Image.fromarray(canvas)
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = WeavePatternGeneratorApp(root)
    root.mainloop()


# In[ ]:





# In[ ]:




