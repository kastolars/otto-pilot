import tkinter as tk
from copilot_capture import Capturer
from threading import Thread

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 300


class Gui:

    def __init__(self):
        self.is_capturing = False

    def _capture(self):
        if self.is_capturing:
            self.capture_text.set("Capture")
            self.is_capturing = False
            self.cap.terminate()
        else:
            self.capture_text.set("Done")
            self.is_capturing = True
            t = Thread(target=self.cap.run)
            t.start()

    def _fstore(self, events):
        with open('events.json', 'w') as f:
            f.write(events)
            f.close()

    def run(self):
        self.window = tk.Tk()
        self.window.title("Copilot")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(0, 0)

        self.capture_text = tk.StringVar()
        capture_button = tk.Button(self.window,
                                   textvariable=self.capture_text,
                                   command=self._capture)
        self.capture_text.set("Capture")
        self.cap = Capturer(fstore=self._fstore)
        capture_button.pack()

        self.window.mainloop()


if __name__ == "__main__":
    g = Gui()
    g.run()
