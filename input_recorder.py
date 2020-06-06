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

# TODO: dump to file
# https://pypi.org/project/dataclasses-json/
# json_events = Event.schema().loads(events, many=True)
# print(json_events)

iterations = 1
try:
    iterations = int(input('Run how many iterations? '))
except ValueError:
    iterations = 1

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

try:
    last_timestamp = events[0].timestamp
except IndexError:
    logging.error('No events were recorded')
    exit(1)

try:
    for i in range(iterations):
        for event in events:
            event_timestamp = event.timestamp
            delay = event_timestamp - last_timestamp
            print(delay)
            time.sleep(delay)
            if event.mouse_event:
                mouse_controller.position = (event.x, event.y)
                if event.pressed:
                    mouse_controller.click(event.button)
                else:
                    mouse_controller.release(event.button)
            else:
                if event.pressed:
                    keyboard_controller.press(event.key)
                else:
                    keyboard_controller.release(event.key)
            last_timestamp = event_timestamp
        last_timestamp = events[0].timestamp
except KeyboardInterrupt:
    print('Exiting!')