from pynput import mouse, keyboard
import time
from dataclasses import dataclass
import logging
from dataclasses_json import dataclass_json, LetterCase
import threading
from typing import Optional

logging.basicConfig(level=logging.INFO)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Event:
    timestamp: int
    pressed: bool
    x: Optional[int] = None
    y: Optional[int] = None
    button: Optional[int] = None
    key: Optional[str] = None


class Capturer:

    def __init__(self, fstore):
        self.events = []
        self.fstore = fstore

    def _on_click(self, x, y, button, pressed):
        timestamp = time.time()
        action = 'pressed' if pressed else 'released'
        logging.info(f'{button} {action} at {x},{y}.')
        button = mouse.Button(button).value
        event = Event(
            timestamp,
            pressed,
            x,
            y,
            button
        )
        self.events.append(event)

    def _stop_listener(self):
        logging.info("Stop listener invoked")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt detected.")
            self.mouse_listener.stop()
            return

    def _on_press(self, key):
        try:
            timestamp = time.time()
            event = Event(timestamp=timestamp, pressed=True, key=key)
            self.events.append(event)
            logging.info(f'{key} key pressed')
        except AttributeError:
            logging.info(f'Attribute error raised by key {key}')

    def _on_release(self, key):
        timestamp = time.time()
        event = Event(timestamp=timestamp, pressed=False, key=key)
        self.events.append(event)
        logging.info(f'{key} key released')
        self._stop_esc(key)

    def terminate(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def _stop_esc(self, key):
        if key == keyboard.Key.esc:
            self.terminate()

    def run(self):
        logging.info("Begin capture.")
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release)
        with self.mouse_listener, self.keyboard_listener:
            self.mouse_listener.join()
            self.keyboard_listener.join()

        logging.info("Terminating capture.")

        events = Event.schema().dumps(self.events, many=True)
        self.fstore(events)


def fstore(events):
    with open('events.json', 'w') as f:
        f.write(events)
        f.close()


if __name__ == "__main__":
    c = Capturer(fstore)
    c.run()
