import tkinter as tk
import sys
from capture import Capturer, Event
from control import Controller
from threading import Thread
from tkinter.filedialog import asksaveasfile, askopenfilename
import json


WINDOW_WIDTH = 450
WINDOW_HEIGHT = 300
POPUP_WIDTH = 300
POPUP_HEIGHT = 200


class Gui:

    def __init__(self):
        """
        Initialize capture/control toggles
        """
        self.is_capturing = False
        self.is_controlling = False

    def _capture(self):
        """
        Click handler for capture button
        """
        if self.is_capturing and not self.is_controlling:
            self.capture_text.set("Capture")
            self.cap.terminate()
            self.is_capturing = False
        elif not self.is_capturing and not self.is_controlling:
            self.is_capturing = True
            self.capture_text.set("Done")
            t = Thread(target=self.cap.run)
            t.start()

    def _save_file(self):
        """
        Callback for saving the file
        """
        with asksaveasfile(mode="w", defaultextension=".json") as f:
            f.write(self.events)
            f.close()
            self.popup.destroy()

    def _fstore(self, events):
        """
        Callback for when capture is complete
        """
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

    def _control(self):
        """
        Click handler for control button
        """
        self.window.filename = askopenfilename()
        self.popup = tk.Toplevel()
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.popup.resizable(0, 0)
        label = tk.Label(self.popup, text="Iterations")
        label.pack()
        self.spinbox = tk.Spinbox(self.popup, from_=1, to=sys.maxsize)
        self.spinbox.pack()
        run_button = tk.Button(self.popup,
                               text="Run Jobs",
                               command=self._run_jobs)
        run_button.pack()
        cancel_button = tk.Button(self.popup,
                                  text="Cancel",
                                  command=self.popup.destroy)
        cancel_button.pack()

    def _run_jobs(self):
        """
        Runs the control script with the selected json file
        """
        self.is_controlling = True
        with open(self.window.filename, "r", encoding='utf-8') as f:
            events = Event.schema().load(json.load(f), many=True)
            ctrlr = Controller(events, self.controller_terminate)
            iterations = int(self.spinbox.get())
            t = Thread(target=ctrlr.run, args=[iterations])
            t.start()

    def controller_terminate(self):
        self.is_controlling = False

    def run(self):
        """
        Entrypoint for the program
        """
        self.window = tk.Tk()
        self.window.configure(background='navy')
        self.window.title("OttoPilot")
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
                                 command=self._control)
        pilot_button.configure(background='white')
        self.pilot_text.set("Control")
        pilot_button.pack()

        self.window.mainloop()


if __name__ == "__main__":
    g = Gui()
    g.run()
