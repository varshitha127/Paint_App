def register(app):
    from tools import Tool
    class HighlighterTool(Tool):
        def __init__(self):
            super().__init__('Highlighter')
            self.color = '#00BFFF'
            self.size = 10
            self.last_x = None
            self.last_y = None
        def on_press(self, event, canvas):
            self.last_x, self.last_y = event.x, event.y
        def on_drag(self, event, canvas):
            if self.last_x is not None and self.last_y is not None:
                item_id = canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.color, width=self.size, capstyle='round', smooth=True, stipple='gray50')
                self.last_x, self.last_y = event.x, event.y
                return item_id
            return None
        def on_release(self, event, canvas):
            self.last_x, self.last_y = None, None
            return None
    if hasattr(app, 'canvas') and hasattr(app.canvas, 'tool_manager'):
        app.canvas.tool_manager.add_tool(HighlighterTool()) 