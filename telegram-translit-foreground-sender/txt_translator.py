from json import loads, dumps
from translit_translator import trans

with open("./targets.json", "r", encoding="utf-8") as f:
    targets = loads(f.read())

def get_text(default_user = "me"):
    with open("text.txt", encoding="utf-8") as f:
        text = f.read()
    user, _, new_text = text.partition("\n")
    if user.lower() in targets:
        text = new_text
        user = targets[user]
    elif "=" in user:
        text = new_text
        name, _, user = user.partition("=")
        user = user.strip()
        targets[name.strip()] = user
        with open("./targets.json", "w", encoding="utf-8") as f:
            f.write(dumps(targets))
    else:
        user = default_user
    if text.startswith("en\n"):
        text = trans(text[3:], False)
    else:
        text = trans(text)
    return user, text
