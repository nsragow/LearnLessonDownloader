#!/usr/bin/env python3
import bcrypt
import json
import sys
import re
import os
from Crypto.Cipher import AES
from Crypto import Random

# config exits exit

config_data = {}


def default_input(msg: str, default=None):
    result = input(msg)
    if result == "":
        assert default is not None
        return default
    return result


print("user configuration (required):")
em = default_input("email: ")
if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", em):
    print("invalid email %s" % em)
    sys.exit()
pw = default_input("password: ")

print("leave blank if you wish to configure manually:")
first_lesson = default_input("url of first lesson to pull: ", "")
clone_to_path = default_input("path to clone lessons to: ", "")
lesson_count = int(default_input("number of lessons to pull (default 10): ", 10))
web_driver_path = default_input("path to web driver: ", "")
browser = default_input(
    "type of browser you will use(default: chrome, firefox):", "chrome"
)
idle_time = default_input("time in sec between browser actions (default 1.5s)", 1.5)

key = b"Sixteen byte key"
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
pweb = iv + cipher.encrypt(str.encode(pw))

config_data["email"] = em
config_data["password"] = pweb.hex()
config_data["first_lesson"] = first_lesson
config_data["clone_to_path"] = clone_to_path
config_data["lesson_count"] = lesson_count
config_data["web_driver_path"] = web_driver_path
config_data["browser"] = browser
config_data["idle_time"] = idle_time

fm = "x"
if os.path.isfile("config.json"):
    fm = "w"
with open("config.json", fm) as cfg:
    json.dump(config_data, cfg, indent=4)
