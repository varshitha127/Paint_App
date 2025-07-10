"""
tools.py - Tool management for the Paint App
"""

from shapes import Rectangle, Oval
import random

class Tool:
    """
    Base class for drawing tools (brush, eraser, etc.).
    """
    def __init__(self, name):
        self.name = name

    def on_press(self, event, canvas):
        pass

    def on_drag(self, event, canvas):
        pass

    def on_release(self, event, canvas):
        pass

class BrushTool(Tool):
    """
    Brush tool for freehand drawing.
    """
    def __init__(self, color='black', size=3):
        super().__init__('Brush')
        self.color = color
        self.size = size
        self.last_x = None
        self.last_y = None

    def on_press(self, event, canvas):
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event, canvas):
        if self.last_x is not None and self.last_y is not None:
            item_id = canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.color, width=self.size, capstyle='round', smooth=True)
            self.last_x, self.last_y = event.x, event.y
            return item_id
        return None

    def on_release(self, event, canvas):
        self.last_x, self.last_y = None, None
        return None

class EraserTool(Tool):
    """
    Eraser tool for erasing drawings.
    """
    def __init__(self, size=10):
        super().__init__('Eraser')
        self.size = size
        self.last_x = None
        self.last_y = None

    def on_press(self, event, canvas):
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event, canvas):
        if self.last_x is not None and self.last_y is not None:
            item_id = canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='white', width=self.size, capstyle='round', smooth=True)
            self.last_x, self.last_y = event.x, event.y
            return item_id
        return None

    def on_release(self, event, canvas):
        self.last_x, self.last_y = None, None
        return None

class RectangleTool(Tool):
    """
    Tool for drawing rectangles.
    """
    def __init__(self, color='black', size=3):
        super().__init__('Rectangle')
        self.color = color
        self.size = size
        self.start = None
        self.temp_shape_id = None

    def on_press(self, event, canvas):
        self.start = (event.x, event.y)
        self.temp_shape_id = None

    def on_drag(self, event, canvas):
        if self.start:
            if self.temp_shape_id:
                canvas.delete(self.temp_shape_id)
            rect = Rectangle(self.start, (event.x, event.y))
            self.temp_shape_id = rect.draw(canvas, outline=self.color, width=self.size, temp=True)
        return self.temp_shape_id

    def on_release(self, event, canvas):
        if self.start:
            if self.temp_shape_id:
                canvas.delete(self.temp_shape_id)
            rect = Rectangle(self.start, (event.x, event.y))
            item_id = rect.draw(canvas, outline=self.color, width=self.size)
            self.start = None
            self.temp_shape_id = None
            return item_id
        return None

class OvalTool(Tool):
    """
    Tool for drawing ovals.
    """
    def __init__(self, color='black', size=3):
        super().__init__('Oval')
        self.color = color
        self.size = size
        self.start = None
        self.temp_shape_id = None

    def on_press(self, event, canvas):
        self.start = (event.x, event.y)
        self.temp_shape_id = None

    def on_drag(self, event, canvas):
        if self.start:
            if self.temp_shape_id:
                canvas.delete(self.temp_shape_id)
            oval = Oval(self.start, (event.x, event.y))
            self.temp_shape_id = oval.draw(canvas, outline=self.color, width=self.size, temp=True)
        return self.temp_shape_id

    def on_release(self, event, canvas):
        if self.start:
            if self.temp_shape_id:
                canvas.delete(self.temp_shape_id)
            oval = Oval(self.start, (event.x, event.y))
            item_id = oval.draw(canvas, outline=self.color, width=self.size)
            self.start = None
            self.temp_shape_id = None
            return item_id
        return None

class LineTool(Tool):
    """
    Tool for drawing straight lines.
    """
    def __init__(self, color='black', size=3):
        super().__init__('Line')
        self.color = color
        self.size = size
        self.start = None
        self.temp_line_id = None

    def on_press(self, event, canvas):
        self.start = (event.x, event.y)
        self.temp_line_id = None

    def on_drag(self, event, canvas):
        if self.start:
            if self.temp_line_id:
                canvas.delete(self.temp_line_id)
            self.temp_line_id = canvas.create_line(self.start[0], self.start[1], event.x, event.y, fill=self.color, width=self.size)
        return self.temp_line_id

    def on_release(self, event, canvas):
        if self.start:
            if self.temp_line_id:
                canvas.delete(self.temp_line_id)
            item_id = canvas.create_line(self.start[0], self.start[1], event.x, event.y, fill=self.color, width=self.size)
            self.start = None
            self.temp_line_id = None
            return item_id
        return None

class TextTool(Tool):
    """
    Tool for placing text.
    """
    def __init__(self, color='black', size=16):
        super().__init__('Text')
        self.color = color
        self.size = size

    def on_press(self, event, canvas):
        from tkinter.simpledialog import askstring
        text = askstring("Text Tool", "Enter text:")
        if text:
            item_id = canvas.create_text(event.x, event.y, text=text, fill=self.color, font=("Comic Sans MS", self.size, "bold"))
            return item_id
        return None

    def on_drag(self, event, canvas):
        return None

    def on_release(self, event, canvas):
        return None

class StampTool(Tool):
    """
    Tool for placing random emojis.
    """
    def __init__(self):
        super().__init__('Stamp')
        self.emojis = ['🌟', '⭐', '✨', '🎈', '🎉', '💖', '🐱', '🐶', '🦄', '🍕', '🍦', '🚗', '🌈', '👑', '🦋']

    def on_press(self, event, canvas):
        emoji = random.choice(self.emojis)
        item_id = canvas.create_text(event.x, event.y, text=emoji, font=("Comic Sans MS", 32))
        return item_id

    def on_drag(self, event, canvas):
        return None

    def on_release(self, event, canvas):
        return None

class ToolManager:
    """
    Manages available tools and current tool selection.
    """
    def __init__(self):
        self.tools = {}
        self.current_tool = None
        self.add_tool(BrushTool())
        self.add_tool(EraserTool())
        self.add_tool(RectangleTool())
        self.add_tool(OvalTool())
        self.add_tool(LineTool())
        self.add_tool(TextTool())
        self.add_tool(StampTool())
        self.select_tool('Brush')

    def add_tool(self, tool):
        self.tools[tool.name] = tool

    def select_tool(self, name):
        self.current_tool = self.tools.get(name) 