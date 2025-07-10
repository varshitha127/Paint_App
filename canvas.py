"""
canvas.py - Drawing logic for the Paint App
"""

import tkinter as tk
from tools import ToolManager
from shapes import Shape, Rectangle, Oval
import random

class PaintCanvas(tk.Canvas):
    """
    Canvas widget for drawing. Handles mouse events, drawing logic, and manages multiple layers.
    Supports adding, switching, and managing visibility of layers.
    """
    def __init__(self, parent, **kwargs):
        """Initialize the PaintCanvas with tool manager, event bindings, and layer management."""
        super().__init__(parent, bg='white', **kwargs)
        self.tool_manager = ToolManager()
        self._bind_events()
        self.undo_stack = []
        self.redo_stack = []
        self._recording = True
        self.layers = [self]
        self.current_layer = 0
        self.shapes = []
        self.selected_shape = None
        self.selection_mode = False
        self._drag_offset = (0, 0)
        self._resize_mode = False
        self.bg_color = 'white'

    def set_background(self, color):
        """Set the background color of the canvas and all layers."""
        self.bg_color = color
        self.config(bg=color)

    def random_color(self):
        """Set a random color for the current tool and return it."""
        color = random.choice(['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff69b4', '#ffa500', '#800080', '#b5ead7', '#f7cac9', '#e0bbff', '#ffe066', '#c3f584'])
        self.tool_manager.current_tool.color = color
        return color

    def random_tool(self):
        """Select a random tool and return its name."""
        tool = random.choice(list(self.tool_manager.tools.values()))
        self.tool_manager.current_tool = tool
        return tool.name

    def _bind_events(self):
        """Bind mouse and keyboard events to the canvas."""
        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<B1-Motion>', self._on_drag)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Delete>', self._on_delete)
        self.focus_set()

    def _on_press(self, event):
        """Handle mouse press event for drawing or selecting shapes."""
        if self.selection_mode:
            self._select_shape(event.x, event.y)
            if self.selected_shape:
                self._drag_offset = (event.x - self.selected_shape.start[0], event.y - self.selected_shape.start[1])
        else:
            tool = self.tool_manager.current_tool
            if tool:
                item_id = tool.on_press(event, self)
                if self._recording and item_id:
                    self._current_action = [item_id]
                else:
                    self._current_action = []
            else:
                self._current_action = []
            self._recording = True

    def _on_drag(self, event):
        """Handle mouse drag event for drawing or moving shapes."""
        if self.selection_mode and self.selected_shape:
            dx = event.x - self.selected_shape.start[0] - self._drag_offset[0]
            dy = event.y - self.selected_shape.start[1] - self._drag_offset[1]
            self.selected_shape.move(dx, dy)
            self.selected_shape.draw(self)
        else:
            tool = self.tool_manager.current_tool
            if tool:
                item_id = tool.on_drag(event, self)
                if self._recording and item_id:
                    self._current_action.append(item_id)
                if getattr(tool, 'name', None) == 'Brush':
                    self._draw_sparkle(event.x, event.y, tool.color)

    def _on_release(self, event):
        """Handle mouse release event for drawing completion."""
        if self.selection_mode:
            pass
        else:
            tool = self.tool_manager.current_tool
            if tool:
                item_id = tool.on_release(event, self)
                if self._recording and item_id:
                    self._current_action.append(item_id)
            if self._recording and self._current_action:
                self.undo_stack.append(self._current_action)
                self.redo_stack.clear()
            self._recording = False
            self._current_action = []
        # Update status bar if present
        if hasattr(self.master, 'statusbar'):
            self.master._update_statusbar()

    def _on_delete(self, event):
        """Handle delete key event to remove selected shape."""
        if self.selected_shape:
            self.selected_shape.delete(self)
            self.shapes = [s for s in self.shapes if s != self.selected_shape]
            self._deselect_shape()

    def _select_shape(self, x, y):
        """Select a shape at the given coordinates, if any."""
        for shape in reversed(self.shapes):
            if shape.contains(x, y):
                self.selected_shape = shape
                shape.selected = True
                shape.draw(self, outline='red', width=3)
                return
        self._deselect_shape()

    def _deselect_shape(self):
        """Deselect the currently selected shape, if any."""
        if self.selected_shape:
            self.selected_shape.selected = False
            self.selected_shape.draw(self)
        self.selected_shape = None

    def undo(self):
        """Undo the last drawing action."""
        if self.undo_stack:
            last_action = self.undo_stack.pop()
            for item_id in last_action:
                self.delete(item_id)
            self.redo_stack.append(last_action)

    def redo(self):
        """Redo the last undone drawing action."""
        if self.redo_stack:
            action = self.redo_stack.pop()
            for item_id in action:
                pass
            self.undo_stack.append(action)

    def _draw_sparkle(self, x, y, color):
        """Draw a sparkle effect at the given coordinates."""
        sparkle_type = random.choice(['circle', 'star'])
        size = random.randint(6, 12)
        offset_x = random.randint(-6, 6)
        offset_y = random.randint(-6, 6)
        if sparkle_type == 'circle':
            sparkle_id = self.create_oval(x+offset_x, y+offset_y, x+offset_x+size, y+offset_y+size, fill=color, outline='yellow', width=2)
            self.after(300, lambda: self.delete(sparkle_id))
        else:
            sparkle_id1 = self.create_line(x-4, y, x+4, y, fill='yellow', width=2)
            sparkle_id2 = self.create_line(x, y-4, x, y+4, fill='yellow', width=2)
            self.after(300, lambda: (self.delete(sparkle_id1), self.delete(sparkle_id2))) 

    def add_layer(self):
        """Add a new layer (Canvas) on top of the current layers."""
        parent = self.master if hasattr(self, 'master') else self.winfo_toplevel()
        new_layer = tk.Canvas(parent, bg=self.bg_color, highlightthickness=0)
        new_layer.place(x=self.winfo_x(), y=self.winfo_y(), relwidth=1, relheight=1)
        new_layer.name = f"Layer {len(self.layers)+1}"
        new_layer.visible = True
        self.layers.append(new_layer)
        self._update_layer_stack()
        return new_layer

    def switch_layer(self, index):
        """Switch the active layer to the one at the given index."""
        if 0 <= index < len(self.layers):
            self.current_layer = index
            self._update_layer_stack()

    def _update_layer_stack(self):
        """Update stacking order and event bindings for all layers."""
        for i, layer in enumerate(self.layers):
            if hasattr(layer, 'visible') and not layer.visible:
                layer.place_forget()
            else:
                layer.place(x=self.winfo_x(), y=self.winfo_y(), relwidth=1, relheight=1)
                layer.lift()
            # Only the current layer should handle events
            if i == self.current_layer:
                self._bind_events_to_layer(layer)
            else:
                self._unbind_events_from_layer(layer)

    def _bind_events_to_layer(self, layer):
        """Bind drawing events to the given layer."""
        layer.bind('<ButtonPress-1>', self._on_press)
        layer.bind('<B1-Motion>', self._on_drag)
        layer.bind('<ButtonRelease-1>', self._on_release)
        layer.bind('<Delete>', self._on_delete)
        layer.focus_set()

    def _unbind_events_from_layer(self, layer):
        """Unbind drawing events from the given layer."""
        layer.unbind('<ButtonPress-1>')
        layer.unbind('<B1-Motion>')
        layer.unbind('<ButtonRelease-1>')
        layer.unbind('<Delete>') 

    def delete_layer(self, index):
        """Delete the layer at the given index, if more than one layer exists."""
        if len(self.layers) > 1 and 0 <= index < len(self.layers):
            layer = self.layers.pop(index)
            layer.destroy()
            if self.current_layer >= len(self.layers):
                self.current_layer = len(self.layers) - 1
            self._update_layer_stack()

    def move_layer_up(self, index):
        """Move the layer at the given index up in the stack."""
        if 1 <= index < len(self.layers):
            self.layers[index-1], self.layers[index] = self.layers[index], self.layers[index-1]
            self._update_layer_stack()

    def move_layer_down(self, index):
        """Move the layer at the given index down in the stack."""
        if 0 <= index < len(self.layers)-1:
            self.layers[index], self.layers[index+1] = self.layers[index+1], self.layers[index]
            self._update_layer_stack()

    def toggle_layer_visibility(self, index):
        """Toggle the visibility of the layer at the given index."""
        if 0 <= index < len(self.layers):
            layer = self.layers[index]
            layer.visible = not getattr(layer, 'visible', True)
            self._update_layer_stack()

    def rename_layer(self, index, name):
        """Rename the layer at the given index."""
        if 0 <= index < len(self.layers):
            self.layers[index].name = name 