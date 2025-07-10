"""
ui.py - UI layout and controls for the Paint App
"""

import tkinter as tk
from tkinter import ttk
from canvas import PaintCanvas
from tools import ToolManager
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import random

class PaintAppUI:
    """
    Main UI class for the Paint App.
    Sets up the window, menus, toolbars, and canvas.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Paint App")
        self.root.geometry("1000x700")
        self._setup_menu()
        self._setup_toolbar()
        self._setup_canvas()
        self._setup_statusbar()
        self._setup_layer_sidebar()
        self.root.bind('<Control-z>', lambda e: self._undo())
        self.root.bind('<Control-y>', lambda e: self._redo())
        self.root.bind('<Control-s>', lambda e: self._save())

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._new_file)
        file_menu.add_command(label="Open", command=self._open_file)
        file_menu.add_command(label="Save", command=self._save)
        file_menu.add_command(label="Save As", command=self._save_as)
        file_menu.add_command(label="Delete", command=self._delete_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        # Insert menu
        insert_menu = tk.Menu(menubar, tearoff=0)
        insert_menu.add_command(label="Image...", command=self._insert_image)
        insert_menu.add_command(label="Rectangle", command=self._select_rectangle)
        insert_menu.add_command(label="Oval", command=self._select_oval)
        insert_menu.add_command(label="Line", command=self._select_line)
        insert_menu.add_command(label="Text", command=self._select_text)
        insert_menu.add_command(label="Emoji/Stamp", command=self._select_stamp)
        menubar.add_cascade(label="Insert", menu=insert_menu)
        # Design menu
        design_menu = tk.Menu(menubar, tearoff=0)
        design_menu.add_command(label="Change Background", command=self._set_background)
        design_menu.add_command(label="Random Color Theme", command=self._random_color)
        design_menu.add_command(label="Canvas Size...", command=self._set_canvas_size)
        menubar.add_cascade(label="Design", menu=design_menu)
        # Layout menu
        layout_menu = tk.Menu(menubar, tearoff=0)
        layout_menu.add_command(label="Bring Forward", command=self._bring_forward)
        layout_menu.add_command(label="Send Backward", command=self._send_backward)
        layout_menu.add_command(label="Center on Canvas", command=self._center_on_canvas)
        menubar.add_cascade(label="Layout", menu=layout_menu)
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Instructions", command=self._show_instructions)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def _setup_toolbar(self):
        toolbar = tk.Frame(self.root, bd=2, relief=tk.RAISED, bg='#fffbe7')
        playful_font = ("Comic Sans MS", 12, "bold")
        # Tool buttons with emoji icons
        brush_btn = tk.Button(toolbar, text="🖌️ Brush", font=playful_font, bg="#ffb347", command=self._select_brush, width=10, height=2)
        brush_btn.pack(side=tk.LEFT, padx=4, pady=4)
        eraser_btn = tk.Button(toolbar, text="🧽 Eraser", font=playful_font, bg="#b0e0e6", command=self._select_eraser, width=10, height=2)
        eraser_btn.pack(side=tk.LEFT, padx=4, pady=4)
        rectangle_btn = tk.Button(toolbar, text="🔲 Rectangle", font=playful_font, bg="#c3f584", command=self._select_rectangle, width=12, height=2)
        rectangle_btn.pack(side=tk.LEFT, padx=4, pady=4)
        oval_btn = tk.Button(toolbar, text="⚪ Oval", font=playful_font, bg="#f7cac9", command=self._select_oval, width=10, height=2)
        oval_btn.pack(side=tk.LEFT, padx=4, pady=4)
        line_btn = tk.Button(toolbar, text="📏 Line", font=playful_font, bg="#ffe066", command=self._select_line, width=10, height=2)
        line_btn.pack(side=tk.LEFT, padx=4, pady=4)
        text_btn = tk.Button(toolbar, text="🔤 Text", font=playful_font, bg="#b5ead7", command=self._select_text, width=10, height=2)
        text_btn.pack(side=tk.LEFT, padx=4, pady=4)
        stamp_btn = tk.Button(toolbar, text="🌟 Stamp", font=playful_font, bg="#f7cac9", command=self._select_stamp, width=10, height=2)
        stamp_btn.pack(side=tk.LEFT, padx=4, pady=4)
        bg_btn = tk.Button(toolbar, text="🌈 Background", font=playful_font, bg="#e0bbff", command=self._set_background, width=12, height=2)
        bg_btn.pack(side=tk.LEFT, padx=4, pady=4)
        random_btn = tk.Button(toolbar, text="❓ Surprise", font=playful_font, bg="#c3f584", command=self._random_color, width=10, height=2)
        random_btn.pack(side=tk.LEFT, padx=4, pady=4)

        # Color palette
        tk.Label(toolbar, text="Colors:", font=playful_font, bg='#fffbe7').pack(side=tk.LEFT, padx=6)
        self.color_var = tk.StringVar(value="#000000")
        color_palette = [
            ("#ff0000", "Red"), ("#00ff00", "Green"), ("#0000ff", "Blue"), ("#ffff00", "Yellow"),
            ("#ff69b4", "Pink"), ("#ffa500", "Orange"), ("#800080", "Purple"), ("#000000", "Black"), ("#ffffff", "White")
        ]
        for color, name in color_palette:
            btn = tk.Button(toolbar, bg=color, width=3, height=2, relief=tk.RAISED, command=lambda c=color: self._set_color_from_palette(c))
            btn.pack(side=tk.LEFT, padx=2)
            self._add_hover_effect(btn)
        # Color picker dialog
        color_picker_btn = tk.Button(toolbar, text="🎨 More Colors", font=playful_font, bg="#e0bbff", command=self._open_color_picker)
        color_picker_btn.pack(side=tk.LEFT, padx=4)
        self._add_hover_effect(color_picker_btn)

        # Size selection
        tk.Label(toolbar, text="Size:", font=playful_font, bg='#fffbe7').pack(side=tk.LEFT, padx=6)
        self.size_var = tk.IntVar(value=3)
        size_spin = tk.Spinbox(toolbar, from_=1, to=50, textvariable=self.size_var, width=3, font=playful_font, command=self._set_size)
        size_spin.pack(side=tk.LEFT, padx=2)

        # Undo/Redo/Save
        undo_btn = tk.Button(toolbar, text="↩️ Undo", font=playful_font, bg="#ffe066", command=self._undo, width=8, height=2)
        undo_btn.pack(side=tk.LEFT, padx=4, pady=4)
        redo_btn = tk.Button(toolbar, text="↪️ Redo", font=playful_font, bg="#ffe066", command=self._redo, width=8, height=2)
        redo_btn.pack(side=tk.LEFT, padx=4, pady=4)
        save_btn = tk.Button(toolbar, text="💾 Save", font=playful_font, bg="#b5ead7", command=self._save, width=8, height=2)
        save_btn.pack(side=tk.LEFT, padx=4, pady=4)

        add_layer_btn = tk.Button(toolbar, text="➕ Add Layer", font=playful_font, bg="#f7cac9", command=self._add_layer, width=12, height=2)
        add_layer_btn.pack(side=tk.LEFT, padx=4, pady=4)
        self._add_hover_effect(brush_btn)
        self._add_hover_effect(eraser_btn)
        self._add_hover_effect(rectangle_btn)
        self._add_hover_effect(oval_btn)
        self._add_hover_effect(undo_btn)
        self._add_hover_effect(redo_btn)
        self._add_hover_effect(save_btn)
        self._add_hover_effect(add_layer_btn)
        self._add_hover_effect(line_btn)
        self._add_hover_effect(text_btn)
        self._add_hover_effect(stamp_btn)
        self._add_hover_effect(bg_btn)
        self._add_hover_effect(random_btn)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def _select_brush(self):
        self.canvas.tool_manager.select_tool('Brush')
        self.canvas.config(cursor='pencil')
        self._update_statusbar()

    def _select_eraser(self):
        self.canvas.tool_manager.select_tool('Eraser')
        self.canvas.config(cursor='dotbox')
        self._update_statusbar()

    def _select_rectangle(self):
        self.canvas.tool_manager.select_tool('Rectangle')
        self.canvas.config(cursor='cross')
        self._update_statusbar()

    def _select_oval(self):
        self.canvas.tool_manager.select_tool('Oval')
        self.canvas.config(cursor='circle')
        self._update_statusbar()

    def _set_color(self):
        color = self.color_var.get()
        brush = self.canvas.tool_manager.tools.get('Brush')
        if brush:
            brush.color = color
        self._update_statusbar()

    def _set_size(self):
        size = self.size_var.get()
        brush = self.canvas.tool_manager.tools.get('Brush')
        eraser = self.canvas.tool_manager.tools.get('Eraser')
        if brush:
            brush.size = size
        if eraser:
            eraser.size = size
        self._update_statusbar()

    def _undo(self):
        self.canvas.undo()
        self._update_statusbar()

    def _redo(self):
        self.canvas.redo()
        self._update_statusbar()

    def _save(self):
        try:
            from tkinter import filedialog, simpledialog
            from PIL import ImageGrab
            import os
            filetypes = [('PNG files', '*.png'), ('JPEG files', '*.jpg'), ('SVG files', '*.svg'), ('All files', '*.*')]
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=filetypes)
            if not file_path:
                return
            ext = os.path.splitext(file_path)[1].lower()
            export_bg = simpledialog.askstring("Export Option", "Export with background? (yes/no)")
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            if ext == '.png' or ext == '.jpg':
                img = ImageGrab.grab().crop((x, y, x1, y1))
                if ext == '.jpg':
                    img = img.convert('RGB')
                if export_bg and export_bg.lower().startswith('n'):
                    # Remove background (set to transparent for PNG)
                    if ext == '.png':
                        img = img.convert('RGBA')
                        datas = img.getdata()
                        newData = [(r, g, b, 0) if (r, g, b) == (255, 255, 255) else (r, g, b, a) for (r, g, b, *a) in datas]
                        img.putdata(newData)
                img.save(file_path)
            elif ext == '.svg':
                try:
                    import svgwrite
                    dwg = svgwrite.Drawing(file_path, size=(self.canvas.winfo_width(), self.canvas.winfo_height()))
                    # Only export shapes for now
                    for shape in getattr(self.canvas, 'shapes', []):
                        if isinstance(shape, Rectangle):
                            dwg.add(dwg.rect(insert=shape.start, size=(shape.end[0]-shape.start[0], shape.end[1]-shape.start[1]), stroke='black', fill='none'))
                        elif isinstance(shape, Oval):
                            dwg.add(dwg.ellipse(center=((shape.start[0]+shape.end[0])/2, (shape.start[1]+shape.end[1])/2), r=((abs(shape.end[0]-shape.start[0])/2), abs(shape.end[1]-shape.start[1])/2), stroke='black', fill='none'))
                    dwg.save()
                except ImportError:
                    print("svgwrite not installed. SVG export unavailable.")
        except Exception as e:
            print(f"Error saving image: {e}")

    def _setup_canvas(self):
        self.canvas = PaintCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _setup_statusbar(self):
        self.statusbar = tk.Label(self.root, text="Tool: Brush | Color: #000000 | Size: 3", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Comic Sans MS", 10), bg="#fffbe7")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _update_statusbar(self):
        tool = self.canvas.tool_manager.current_tool.name if self.canvas.tool_manager.current_tool else "None"
        color = self.color_var.get()
        size = self.size_var.get()
        self.statusbar.config(text=f"Tool: {tool} | Color: {color} | Size: {size}")

    def _setup_layer_sidebar(self):
        sidebar = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(sidebar, text="Layers").pack()
        self.layer_listbox = tk.Listbox(sidebar)
        self.layer_listbox.pack(fill=tk.BOTH, expand=True)
        self._refresh_layer_list()
        btn_frame = tk.Frame(sidebar)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Add", command=self._add_layer).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Delete", command=self._delete_layer).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Up", command=self._move_layer_up).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Down", command=self._move_layer_down).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Hide/Show", command=self._toggle_layer_visibility).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Rename", command=self._rename_layer).pack(side=tk.LEFT)
        self.layer_listbox.bind('<<ListboxSelect>>', self._on_layer_select)

    def _refresh_layer_list(self):
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.canvas.layers):
            name = getattr(layer, 'name', f"Layer {i+1}")
            visible = getattr(layer, 'visible', True)
            self.layer_listbox.insert(tk.END, f"{name}{' (hidden)' if not visible else ''}")

    def _add_layer(self):
        """Add a new layer to the canvas and refresh the layer list."""
        new_layer = self.canvas.add_layer()
        new_layer.name = f"Layer {len(self.canvas.layers)}"
        new_layer.visible = True
        self._refresh_layer_list()

    def _delete_layer(self):
        """Delete the selected layer using the canvas method and refresh the list."""
        idx = self.layer_listbox.curselection()
        if idx and len(self.canvas.layers) > 1:
            idx = idx[0]
            self.canvas.delete_layer(idx)
            self._refresh_layer_list()

    def _move_layer_up(self):
        """Move the selected layer up using the canvas method and refresh the list."""
        idx = self.layer_listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.canvas.move_layer_up(i)
            self._refresh_layer_list()

    def _move_layer_down(self):
        """Move the selected layer down using the canvas method and refresh the list."""
        idx = self.layer_listbox.curselection()
        if idx and idx[0] < len(self.canvas.layers)-1:
            i = idx[0]
            self.canvas.move_layer_down(i)
            self._refresh_layer_list()

    def _toggle_layer_visibility(self):
        """Toggle visibility of the selected layer using the canvas method and refresh the list."""
        idx = self.layer_listbox.curselection()
        if idx:
            i = idx[0]
            self.canvas.toggle_layer_visibility(i)
            self._refresh_layer_list()

    def _rename_layer(self):
        """Rename the selected layer using the canvas method and refresh the list."""
        idx = self.layer_listbox.curselection()
        if idx:
            i = idx[0]
            name = tk.simpledialog.askstring("Rename Layer", "New name:")
            if name:
                self.canvas.rename_layer(i, name)
                self._refresh_layer_list()

    def _on_layer_select(self, event):
        idx = self.layer_listbox.curselection()
        if idx:
            self.canvas.switch_layer(idx[0]) 

    def _add_hover_effect(self, btn):
        def on_enter(e):
            btn.config(relief=tk.SUNKEN, bd=4)
        def on_leave(e):
            btn.config(relief=tk.RAISED, bd=2)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _set_color_from_palette(self, color):
        self.color_var.set(color)
        self._set_color()
        self._update_statusbar()

    def _open_color_picker(self):
        from tkinter import colorchooser
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.color_var.set(color_code)
            self._set_color() 
            self._update_statusbar()

    def _select_line(self):
        self.canvas.tool_manager.select_tool('Line')
        self.canvas.config(cursor='cross')
        self._update_statusbar()

    def _select_text(self):
        self.canvas.tool_manager.select_tool('Text')
        self.canvas.config(cursor='xterm')
        self._update_statusbar()

    def _select_stamp(self):
        self.canvas.tool_manager.select_tool('Stamp')
        self.canvas.config(cursor='dotbox')
        self._update_statusbar()

    def _set_background(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Choose background color")[1]
        if color:
            self.canvas.set_background(color)
            self._update_statusbar()

    def _random_color(self):
        color = self.canvas.random_color()
        self.color_var.set(color)
        self._set_color()
        self._update_statusbar()

    # --- File operations ---
    def _new_file(self):
        if tkinter.messagebox.askyesno("New File", "Start a new drawing? Unsaved work will be lost."):
            self.canvas.delete("all")
    def _open_file(self):
        file_path = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
            self._opened_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self._opened_img)
    def _save_as(self):
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('JPEG files', '*.jpg'), ('All files', '*.*')])
        if file_path:
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            img = ImageGrab.grab().crop((x, y, x1, y1))
            img.save(file_path)
    def _delete_file(self):
        file_path = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if file_path and tkinter.messagebox.askyesno("Delete File", f"Delete {os.path.basename(file_path)}?"):
            os.remove(file_path)
            tkinter.messagebox.showinfo("Deleted", "File deleted.") 

    # --- Insert menu actions ---
    def _insert_image(self):
        from tkinter import filedialog
        from PIL import Image, ImageTk
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((100, 100))
            self._inserted_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(50, 50, anchor=tk.NW, image=self._inserted_img)

    # --- Design menu actions ---
    def _set_canvas_size(self):
        from tkinter.simpledialog import askinteger
        width = askinteger("Canvas Width", "Enter new width:", initialvalue=self.canvas.winfo_width())
        height = askinteger("Canvas Height", "Enter new height:", initialvalue=self.canvas.winfo_height())
        if width and height:
            self.canvas.config(width=width, height=height)

    # --- Layout menu actions (placeholders) ---
    def _bring_forward(self):
        pass  # Placeholder for future layer/object ordering
    def _send_backward(self):
        pass  # Placeholder for future layer/object ordering
    def _center_on_canvas(self):
        pass  # Placeholder for future centering logic

    # --- Help menu actions ---
    def _show_about(self):
        tk.messagebox.showinfo("About", "Paint Party!\nA playful drawing app for everyone.")
    def _show_instructions(self):
        tk.messagebox.showinfo("Instructions", "Use the toolbar and menus to draw, insert, and design!\nTry the fun features like emoji stamps and surprise tool.") 