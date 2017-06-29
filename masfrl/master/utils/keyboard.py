"""
    Module that takes care of keyboard listeners
"""

from pynput import keyboard


def listen_for_enter():
    """
    Creates a keyboard listener for the current python process,
    and adds a handler to notify on ENTER.
    :return: Exits once key was pressed
    """
    def on_press(key):
        if key == keyboard.Key.enter:
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
