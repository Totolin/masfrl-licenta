from pynput import keyboard


def listen_for_enter():
    def on_press(key):
        if key == keyboard.Key.enter:
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
