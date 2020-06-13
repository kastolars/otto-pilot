import json
import logging
from capture import Event
import time
from pynput import mouse, keyboard

logging.basicConfig(level=logging.INFO)


class Controller:

    def __init__(self, events, terminate_callback):
        self.events = events
        self.terminate_callback = terminate_callback
        for event in self.events:
            if event.button is not None:
                event.button = mouse.Button(event.button)
            if event.key is not None:
                event.key = event.key.replace('\'', '')
                event.key = event.key.replace('Key.', '')
                if event.key in keyboard.Key.__dict__:
                    event.key = keyboard.Key.__dict__[event.key]

    def run(self, iterations=1):
        """
        Entrypoint for the controller
        """
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        try:
            last_timestamp = self.events[0].timestamp
        except IndexError:
            logging.error("No events loaded")
            exit(1)

        try:
            for _ in range(iterations):
                for event in self.events:
                    duration = event.timestamp - last_timestamp
                    time.sleep(duration)
                    if event.key is None:
                        mouse_controller.position = (event.x, event.y)
                        if event.pressed:
                            mouse_controller.click(event.button)
                            logging.info(
                                f'{event.button} pressed at {event.x},{event.y}.')
                        else:
                            mouse_controller.release(event.button)
                            logging.info(
                                f'{event.button} released at {event.x},{event.y}.')
                    else:
                        if event.pressed:
                            keyboard_controller.press(event.key)
                            logging.info(f'{event.key} key pressed')
                        else:
                            keyboard_controller.release(event.key)
                            logging.info(f'{event.key} key released')
                    last_timestamp = event.timestamp
                last_timestamp = self.events[0].timestamp
        except KeyboardInterrupt:
            logging.info("Interrupt detected")
        finally:
            self.terminate_callback()

def terminate():
    logging.info("Terminating")


if __name__ == "__main__":
    with open("events.json", "r") as f:

        events = Event.schema().load(json.load(f), many=True)

        c = Controller(events, terminate)

        c.run()
