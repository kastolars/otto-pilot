import json
import logging
from copilot_capture import Event
import time
from pynput import mouse, keyboard

logging.basicConfig(level=logging.INFO)

BUTTON_MAPPING = {
    "Button.unknown": mouse.Button.unknown,
    "Button.left": mouse.Button.left,
    "Button.middle": mouse.Button.middle,
    "Button.right": mouse.Button.right,
}


class Pilot:

    def __init__(self, events):
        self.events = events

    def run(self):

        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        try:
            last_timestamp = self.events[0].timestamp
        except IndexError:
            logging.error("No events loaded")
            exit(1)

        try:
            for event in self.events:
                duration = event.timestamp - last_timestamp
                time.sleep(duration)
                if event.key is None:
                    mouse_controller.position = (event.x, event.y)
                    if event.pressed:
                        mouse_controller.click(BUTTON_MAPPING[event.button])
                        logging.info(
                            f'{event.button} pressed at {event.x},{event.y}.')
                    else:
                        mouse_controller.release(BUTTON_MAPPING[event.button])
                        logging.info(
                            f'{event.button} released at {event.x},{event.y}.')
                else:
                    if event.pressed:
                        keyboard_controller.press(event.key.replace('\'', ''))
                        logging.info(f'{event.key} key pressed')
                    else:
                        keyboard_controller.release(
                            event.key.replace('\'', ''))
                        logging.info(f'{event.key} key released')
                last_timestamp = event.timestamp
        except KeyboardInterrupt:
            print("Terminating")
            return


if __name__ == "__main__":
    # with open("events.json", "r") as f:

    #     events = Event.schema().load(json.load(f), many=True)

    # p = Pilot(events)
    # p.run()

    # for btn in mouse.Button.__members__.items():
    #     print(btn)

    print(repr(mouse.Button['unknown']))

    print(keyboard.KeyCode['a'])

    # for key in keyboard.Key.__members__.items():
    #     name = key[0]
    #     print(name)
    #     print(keyboard.Key[name])
