from pynput import mouse, keyboard


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))


def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))


def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        mouse_listener.stop()
        return False


# Collect events until released
with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, \
        keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()
