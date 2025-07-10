import tkinter as tk
from tkinter import colorchooser
import random

root = tk.Tk()
root.title("Playful Paint")
root.geometry("1000x750")
root.configure(bg="#fffbe7")
root.resizable(False, False)

playful_font = ("Comic Sans MS", 14, "bold")
current_x = 0
current_y = 0
color = "#000000"

# --- Canvas Frame for rounded corners and drop shadow ---
canvas_frame = tk.Frame(root, bg="#e0bbff", bd=0, highlightthickness=0)
canvas_frame.place(x=60, y=120, width=880, height=560)
shadow = tk.Label(root, bg="#d1c4e9")
shadow.place(x=68, y=128, width=880, height=560)
canvas = tk.Canvas(canvas_frame, width=860, height=540, bg="white", bd=0, highlightthickness=8, highlightbackground="#b5ead7")
canvas.place(x=10, y=10)

# --- Color Palette ---
color_palette = [
    ("#ff0000", "Red"), ("#00ff00", "Green"), ("#0000ff", "Blue"), ("#ffff00", "Yellow"),
    ("#ff69b4", "Pink"), ("#ffa500", "Orange"), ("#800080", "Purple"), ("#000000", "Black"), ("#ffffff", "White"),
    ("#b5ead7", "Mint"), ("#f7cac9", "Rose"), ("#e0bbff", "Lavender"), ("#ffe066", "Lemon"), ("#c3f584", "Lime")
]

palette_frame = tk.Frame(root, bg="#fffbe7")
palette_frame.place(x=60, y=40)
tk.Label(palette_frame, text="Colors:", font=playful_font, bg="#fffbe7").pack(side=tk.LEFT, padx=8)

def set_color(c):
    global color
    color = c

for c, name in color_palette:
    btn = tk.Button(palette_frame, bg=c, width=3, height=2, relief=tk.RAISED, command=lambda col=c: set_color(col))
    btn.pack(side=tk.LEFT, padx=2)

def choose_color():
    global color
    col = colorchooser.askcolor(title="Choose color")[1]
    if col:
        color = col

color_picker_btn = tk.Button(palette_frame, text="🎨 More Colors", font=playful_font, bg="#e0bbff", command=choose_color)
color_picker_btn.pack(side=tk.LEFT, padx=8)

# --- Brush size ---
size_var = tk.IntVar(value=5)
size_frame = tk.Frame(root, bg="#fffbe7")
size_frame.place(x=400, y=40)
tk.Label(size_frame, text="Brush Size:", font=playful_font, bg="#fffbe7").pack(side=tk.LEFT, padx=8)
size_spin = tk.Spinbox(size_frame, from_=1, to=50, textvariable=size_var, width=3, font=playful_font)
size_spin.pack(side=tk.LEFT, padx=2)

# --- New Canvas Button ---
def new_canvas():
    canvas.delete("all")

new_btn = tk.Button(root, text="🧽 New Canvas", font=playful_font, bg="#b0e0e6", command=new_canvas, width=12, height=2)
new_btn.place(x=800, y=40)

# --- Drawing logic with sparkle effect ---
def locate_xy(event):
    global current_x, current_y
    current_x = event.x
    current_y = event.y

def add_line(event):
    global current_x, current_y
    sz = size_var.get()
    canvas.create_line((current_x, current_y, event.x, event.y), width=sz, fill=color, capstyle=tk.ROUND, smooth=True)
    # Sparkle effect
    draw_sparkle(event.x, event.y, color)
    current_x, current_y = event.x, event.y

def draw_sparkle(x, y, color):
    sparkle_type = random.choice(['circle', 'star'])
    size = random.randint(6, 12)
    offset_x = random.randint(-6, 6)
    offset_y = random.randint(-6, 6)
    if sparkle_type == 'circle':
        sparkle_id = canvas.create_oval(x+offset_x, y+offset_y, x+offset_x+size, y+offset_y+size, fill=color, outline='yellow', width=2)
        canvas.after(300, lambda: canvas.delete(sparkle_id))
    else:
        sparkle_id1 = canvas.create_line(x-4, y, x+4, y, fill='yellow', width=2)
        sparkle_id2 = canvas.create_line(x, y-4, x, y+4, fill='yellow', width=2)
        canvas.after(300, lambda: (canvas.delete(sparkle_id1), canvas.delete(sparkle_id2)))

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', add_line)

# --- Playful Title ---
title_label = tk.Label(root, text="Paint Party! 🎉", font=("Comic Sans MS", 28, "bold"), fg="#ff69b4", bg="#fffbe7")
title_label.place(x=340, y=0)

root.mainloop()