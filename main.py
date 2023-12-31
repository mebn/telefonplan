import requests
import time
from random import randrange

# See tower here: http://camera.colourbynumbers.org/axis-cgi/jpg/image.cgi

# colors as RGB
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
yellow = [255,255,0]


def get_hash():
    url = "http://api.colourbynumbers.org/cbn-live/requestLock"
    res = requests.get(url).json()
    if res["status"]["code"] == 0:
        return None
    return res["hash"]


def get_hash_while():
    hash = None
    while hash == None:
        hash = get_hash()
        if hash == None:
            print("no hash")
            time.sleep(1)
    return hash


def set_colors(hash, colors):
    url = "http://api.colourbynumbers.org/cbn-live/setColours?hash=" + hash + "&colours=" + str(colors)
    res = requests.get(url).json()
    return res


def get_colors_string(colors):
    s = "{"
    s += f"%220%22%3A[{colors[0][0]}%2C{colors[0][1]}%2C{colors[0][2]}]"
    for i, color in enumerate(colors[1:]):
        s += f"%2C%22{i + 1}%22%3A[{color[0]}%2C{color[1]}%2C{color[2]}]"
    s += "}"
    return s


def random_colors(hash):
    while True:
        random_colors_list = []
        for _ in range(10):
            random_colors_list.append([randrange(256),randrange(256),randrange(256)])
        random_colors = get_colors_string(random_colors_list)

        res = set_colors(hash, random_colors)
        if res["status"]["code"] == 0 and res["status"]["description"] == "invalid hash":
            print("color not set", res)
            return
        time.sleep(1)


def toggle_colors(hash):
    tick = True

    color1 = []
    color2 = []
    for _ in range(10):
        color1.append(blue)
        color2.append(red)
    color1 = get_colors_string(color1)
    color2 = get_colors_string(color2)

    while True:
        color = color1 if tick else color2
        res = set_colors(hash, color)
        if res["status"]["code"] == 0 and res["status"]["description"] == "invalid hash":
            print("color not set", res)
            return
        tick = not tick
        time.sleep(2)


def main():
    while True:
        hash = get_hash_while()
        print(hash)
        random_colors(hash)


if __name__ == "__main__":
    main()
