import clipboard
both = ("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", "йцукенгшщзфывапролдячсмитьЙЦУКЕНГШЩЗФЫВАПРОЛДЯЧСМИТЬ")
en = """`[];',./~{}|:"<>?@#$^&"""
ru = """ёхъжэбю.ЁХЪ/ЖЭБЮ,"№;:?"""

def trans(text: str, en2ru = True) -> str:

    if en2ru:
        additional = dict(zip(en, ru))
    else:
        additional = dict(zip(ru, en))

    translate = dict(zip(*both)) | additional

    return "".join(map(lambda l:translate[l] if l in translate else l, text)).strip()

def main():
    text = r"""

    """

    ans = trans(text)
    clipboard.copy(ans)

if __name__ == "__main__":
    main()