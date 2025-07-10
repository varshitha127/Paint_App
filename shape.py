import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application")

        # Create a canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        # Shape selection
        self.shape = "rectangle"  # Default shape

        # Create buttons for shape selection
        rectangle_button = tk.Button(root, text="Rectangle", command=lambda: self.set_shape("rectangle"))
        rectangle_button.pack(side=tk.LEFT)

        oval_button = tk.Button(root, text="Oval", command=lambda: self.set_shape("oval"))
        oval_button.pack(side=tk.LEFT)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_left_button_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_button_release)

        # Initialize shape drawing variables
        self.start_x = None
        self.start_y = None

    def set_shape(self, shape):
        self.shape = shape

    def on_left_button_click(self, event):
        # Store the starting coordinates
        self.start_x = event.x
        self.start_y = event.y

    def on_left_button_release(self, event):
        # Draw the selected shape on mouse release
        if self.start_x is not None and self.start_y is not None:
            if self.shape == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", fill="")
            elif self.shape == "oval":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black", fill="")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    app.run