from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import system as run_bash
import re
import json
from Crypto.Cipher import AES
from Crypto import Random


config = None
with open("config.json", "r") as cfg:
    config = json.load(cfg)

chromedriver_path = config["web_driver_path"]
# login credentials for learn
username = config["email"]
password_crypt = config["password"]
# the first lesson to clone
start = config["first_lesson"]
# the directory to drop all the files into
clone_to_path = config["clone_to_path"]
# how many lessons to download
lesson_count = config["lesson_count"]
# the type of browser you are using
browser = config["browser"]

key = b"Sixteen byte key"
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
# password = cipher.decrypt(password_crypt.decode("hex"))
password = cipher.decrypt(bytes.fromhex(password_crypt))[len(iv) :].decode()

# driver = webdriver.Chrome(executable_path=chromedriver_path)
driver = None
if browser == "firefox":
    driver = webdriver.Firefox()
if browser == "chrome":
    driver = webdriver.Chrome()

url = "https://learn.co/"
driver.get(url)


login = driver.find_element_by_css_selector("input#user-email.input__field")
password = driver.find_element_by_css_selector("input#user-password.input__field")
login.send_keys(username)
password.send_keys(password_text)
password.send_keys(Keys.RETURN)

time.sleep(1)
driver.get(start)
gitlink = driver.find_element_by_css_selector(
    "a.button--color-grey-faint.button--icon-only"
).get_attribute("href")


proceed_b = "a.js--button.button.module--cloud__button--main"
small_b = "div.js--feature-tour-done-button.js--next-button.status-alert__bubble--with-icon.status-alert__bubble--with-icon--color-inverted.status-alert__bubble--main.hoverable"
big_b = "div.status-alert__button--main.button.button--height-large.button--corners-tight.button--layout-block.js--next-button"

time.sleep(1)


def next_lesson():
    global small_b, big_b, proceed_b
    next_b = driver.find_element_by_css_selector(small_b)

    try:
        next_b.click()
    except:
        print("no small")
        next_b = driver.find_element_by_css_selector(big_b)
        try:
            next_b.click()
        except:
            print("no big")
    try:
        next_b = driver.find_element_by_css_selector(proceed_b)
        next_b.click()
    except:
        print("no proceed")


def get_gitlink():
    return driver.find_element_by_css_selector(
        "a.button--color-grey-faint.button--icon-only"
    ).get_attribute("href")


links = []
for x in range(lesson_count):

    links.append(get_gitlink())
    next_lesson()
    time.sleep(1)

# sys.exit()

for x in range(len(links)):
    next_path = "%s/%03d-%s" % (
        clone_to_path,
        x + 1,
        re.sub(r".+(?<=\/)", "", links[x]),
    )
    run_bash(f"git clone {links[x]} {next_path}")
