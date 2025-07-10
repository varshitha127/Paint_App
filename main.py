"""
main.py - Entry point for the Paint App
"""

from ui import PaintAppUI
import tkinter as tk
import os
import importlib.util


def load_plugins(app):
    plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(plugins_dir):
        return
    for filename in os.listdir(plugins_dir):
        if filename.endswith('.py'):
            plugin_path = os.path.join(plugins_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'register'):
                module.register(app)


def show_splash(root, on_close):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x300+500+250")
    splash.configure(bg='#fffbe7')
    playful_font = ("Comic Sans MS", 22, "bold")
    label = tk.Label(splash, text="Welcome to Paint Party! 🎨", font=playful_font, bg='#fffbe7', fg='#ff69b4')
    label.pack(expand=True)
    # Simple animation: bounce the label
    def bounce(count=0, direction=1):
        y = 120 + 10 * direction * (count % 10)
        label.place(x=30, y=y)
        if count < 20:
            splash.after(50, lambda: bounce(count+1, -direction if count % 10 == 9 else direction))
    label.place(x=30, y=120)
    bounce()
    # After 2 seconds, close splash and show main window
    splash.after(2000, lambda: (splash.destroy(), on_close()))

def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window initially
    def start_app():
        root.deiconify()
        app = PaintAppUI(root)
        load_plugins(app)
    show_splash(root, start_app)
    root.mainloop()


if __name__ == "__main__":
    main() 