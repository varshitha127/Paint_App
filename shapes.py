"""
shapes.py - Shape drawing logic for the Paint App
"""

class Shape:
    """
    Base class for shapes, now supports selection and manipulation.
    """
    _id_counter = 0
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.id = Shape._id_counter
        Shape._id_counter += 1
        self.canvas_id = None
        self.selected = False

    def draw(self, canvas, outline='black', width=3, temp=False):
        # To be implemented by subclasses
        pass

    def contains(self, x, y):
        # To be implemented by subclasses for hit-testing
        return False

    def move(self, dx, dy):
        self.start = (self.start[0] + dx, self.start[1] + dy)
        self.end = (self.end[0] + dx, self.end[1] + dy)

    def resize(self, new_end):
        self.end = new_end

    def delete(self, canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)

class Rectangle(Shape):
    def draw(self, canvas, outline='black', width=3, temp=False):
        if self.canvas_id:
            canvas.delete(self.canvas_id)
        self.canvas_id = canvas.create_rectangle(self.start[0], self.start[1], self.end[0], self.end[1], outline=outline, width=width, dash=(2, 2) if temp else None)
        return self.canvas_id
    def contains(self, x, y):
        x0, y0, x1, y1 = min(self.start[0], self.end[0]), min(self.start[1], self.end[1]), max(self.start[0], self.end[0]), max(self.start[1], self.end[1])
        return x0 <= x <= x1 and y0 <= y <= y1

class Oval(Shape):
    def draw(self, canvas, outline='black', width=3, temp=False):
        if self.canvas_id:
            canvas.delete(self.canvas_id)
        self.canvas_id = canvas.create_oval(self.start[0], self.start[1], self.end[0], self.end[1], outline=outline, width=width, dash=(2, 2) if temp else None)
        return self.canvas_id
    def contains(self, x, y):
        x0, y0, x1, y1 = min(self.start[0], self.end[0]), min(self.start[1], self.end[1]), max(self.start[0], self.end[0]), max(self.start[1], self.end[1])
        # Simple bounding box check for now
        return x0 <= x <= x1 and y0 <= y <= y1 