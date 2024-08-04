from foreground_title import foreground_title
import asyncio
from threading import Thread
from telegram_auto import full_send
from pynput import keyboard
from txt_translator import get_text

activated = False
def on_press(key):
    global activated
    if not foreground_title().startswith("text.txt"):
        return None
    if key == keyboard.Key.esc:
        return False
    if key in [keyboard.Key.enter]:
        if activated:
            print("sending a message")
            user, text = get_text()
            asyncio.run_coroutine_threadsafe(full_send(user, text), loop=asyncio.new_event_loop())
    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        activated = True
    else:
        activated = False

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def main():
    keyboard_thread = Thread(target=start_listener)
    keyboard_thread.start()

    # Run the asyncio event loop in the main thread
    asyncio.get_event_loop().run_forever()
if __name__ == "__main__":
    main()