import ctypes

user32 = ctypes.windll.user32
title_length = 255
title = ctypes.create_unicode_buffer(title_length + 1)

def foreground_title() -> str:
    hwnd = user32.GetForegroundWindow()
    user32.GetWindowTextW(hwnd, title, title_length + 1)
    return title.value

if __name__ == "__main__":
    print(foreground_title())