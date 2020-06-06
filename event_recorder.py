from pynput import mouse, keyboard
import time
from dataclasses import dataclass
import logging
from dataclasses_json import dataclass_json, LetterCase

logging.basicConfig(level=logging.INFO)
events = []

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Event:
    mouse_event: bool
    timestamp: int
    pressed: bool
    x: int = None
    y: int = None
    button: str = None
    key: str = None

def on_click(x, y, button, pressed):
    timestamp = time.time()
    events.append(
        Event(mouse_event=True, x=x, y=y, timestamp=timestamp,
              pressed=pressed, button=button)
    )
    action = 'pressed' if pressed else 'released'
    logging.info(f'{button} {action} on {x}, {y}')


def on_press(key):
    try:
        if key == keyboard.Key.esc: return
        timestamp = time.time()
        events.append(
            Event(mouse_event=False, timestamp=timestamp, pressed=True, key=key)
        )
        logging.info(f'{key} key pressed')
    except AttributeError:
        logging.info(f'Attribute error raised by key {key}')


def on_release(key):
    if key == keyboard.Key.esc:
        mouse_listener.stop()
        logging.info('Terminating!')
        return False
    timestamp = time.time()
    events.append(
        Event(mouse_event=False, timestamp=timestamp, pressed=False, key=key)
    )
    logging.info(f'{key} key released')

logging.info('Begin listening')

with mouse.Listener(on_click=on_click) as mouse_listener, \
        keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()