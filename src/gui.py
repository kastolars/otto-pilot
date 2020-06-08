import tkinter as tk
import sys
from capture import Capturer, Event
from control import Pilot
from threading import Thread
from tkinter.filedialog import asksaveasfile, askopenfilename
import json


WINDOW_WIDTH = 450
WINDOW_HEIGHT = 300
POPUP_WIDTH = 300
POPUP_HEIGHT = 200


class Gui:

    def __init__(self):
        self.is_capturing = False
        # TODO: prevent pilot looping on capture button
        self.is_piloting = False

    def _capture(self):
        if self.is_capturing:
            self.capture_text.set("Capture")
            self.cap.terminate()
            self.is_capturing = False
        else:
            self.is_capturing = True
            self.capture_text.set("Done")
            t = Thread(target=self.cap.run)
            t.start()

    def _save_file(self):
        with asksaveasfile(mode="w", defaultextension=".json") as f:
            f.write(self.events)
            f.close()
            self.popup.destroy()

    def _fstore(self, events):
        self.events = events
        self.popup = tk.Toplevel()
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.popup.resizable(0, 0)
        label = tk.Label(self.popup, text="Save file as")
        label.pack()
        save_button = tk.Button(self.popup, text="Save",
                                command=self._save_file)
        save_button.pack()
        cancel_button = tk.Button(self.popup,
                                  text="Cancel",
                                  command=self.popup.destroy)
        cancel_button.pack()

    def _pilot(self):
        self.window.filename = askopenfilename()
        self.popup = tk.Toplevel()
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.popup.resizable(0, 0)
        label = tk.Label(self.popup, text="Iterations")
        label.pack()
        self.spinbox = tk.Spinbox(self.popup, from_=1, to=sys.maxsize)
        self.spinbox.pack()
        run_button = tk.Button(self.popup,
                               text="Run Job",
                               command=self._run_jobs)
        run_button.pack()
        cancel_button = tk.Button(self.popup,
                                  text="Cancel",
                                  command=self.popup.destroy)
        cancel_button.pack()

    def _run_jobs(self):
        self.is_piloting = True
        with open(self.window.filename, "r", encoding='utf-8') as f:
            events = Event.schema().load(json.load(f), many=True)
            pil = Pilot(events)
            iterations = int(self.spinbox.get())
            t = Thread(target=pil.run, args=[iterations])
            t.start()
            t.join()
            self.is_piloting = False

    def run(self):
        self.window = tk.Tk()
        self.window.configure(background='navy')
        self.window.title("Copilot")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(0, 0)

        self.capture_text = tk.StringVar()
        capture_button = tk.Button(self.window,
                                   textvariable=self.capture_text,
                                   command=self._capture)
        capture_button.configure(background='white')
        self.capture_text.set("Capture")
        self.cap = Capturer(fstore=self._fstore)
        capture_button.pack()

        self.pilot_text = tk.StringVar()
        pilot_button = tk.Button(self.window,
                                 textvariable=self.pilot_text,
                                 command=self._pilot)
        pilot_button.configure(background='white')
        self.pilot_text.set("Pilot")
        pilot_button.pack()

        self.window.mainloop()


if __name__ == "__main__":
    g = Gui()
    g.run()
