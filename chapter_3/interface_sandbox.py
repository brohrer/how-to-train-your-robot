from getkey import getkey

while True:
    key = getkey()

    if key in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print(f"key pressed: {key}")
