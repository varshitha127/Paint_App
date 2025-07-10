import unittest
from tools import BrushTool, EraserTool
from canvas import PaintCanvas
import tkinter as tk

class DummyCanvas:
    def __init__(self):
        self.lines = []
    def create_line(self, x0, y0, x1, y1, **kwargs):
        self.lines.append((x0, y0, x1, y1, kwargs))
        return len(self.lines)

class DummyRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Hide the main window

def test_layer_switching():
    root = DummyRoot()
    canvas = PaintCanvas(root)
    initial_layer_count = len(canvas.layers)
    canvas.add_layer()
    assert len(canvas.layers) == initial_layer_count + 1
    canvas.switch_layer(1)
    assert canvas.current_layer == 1
    canvas.switch_layer(0)
    assert canvas.current_layer == 0
    root.destroy()

class TestTools(unittest.TestCase):
    def test_brush_draw(self):
        tool = BrushTool(color='red', size=5)
        canvas = DummyCanvas()
        tool.on_press(type('Event', (), {'x': 10, 'y': 10})(), canvas)
        item_id = tool.on_drag(type('Event', (), {'x': 20, 'y': 20})(), canvas)
        self.assertEqual(len(canvas.lines), 1)
        self.assertEqual(canvas.lines[0][4]['fill'], 'red')
        self.assertEqual(canvas.lines[0][4]['width'], 5)
    def test_eraser_draw(self):
        tool = EraserTool(size=8)
        canvas = DummyCanvas()
        tool.on_press(type('Event', (), {'x': 5, 'y': 5})(), canvas)
        item_id = tool.on_drag(type('Event', (), {'x': 15, 'y': 15})(), canvas)
        self.assertEqual(len(canvas.lines), 1)
        self.assertEqual(canvas.lines[0][4]['fill'], 'white')
        self.assertEqual(canvas.lines[0][4]['width'], 8)

if __name__ == '__main__':
    unittest.main() 