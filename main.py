#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import system as run_bash
import re
import json
import sys
import atexit
import auth

# load the config
config = None
with open("config.json", "r") as cfg:
    config = json.load(cfg)

# config variables
username = config["email"]
password_crypt = config["password"]

chromedriver_path = config["web_driver_path"]
browser = config["browser"]

clone_to_path = config["clone_to_path"]
first_lesson = config["first_lesson"]
last_lesson = config["last_lesson"]
lesson_count = config["lesson_count"]
idle_time = config["idle_time"]


# buttons that could lead to the next page
proceed_b = "a.js--button.button.module--cloud__button--main"
small_b = "div.js--feature-tour-done-button.js--next-button.status-alert__bubble--with-icon.status-alert__bubble--with-icon--color-inverted.status-alert__bubble--main.hoverable"
big_b = "div.status-alert__button--main.button.button--height-large.button--corners-tight.button--layout-block.js--next-button"


def main():
    password = None
    try:
        password = auth.decrypt(password_crypt)
    except:
        print("invalid credentials")
        sys.exit()

    # get a driver for the specified browser and defer the closing of the browser
    # to the exit of the program
    driver = None
    if browser == "firefox":
        driver = webdriver.Firefox()
    if browser == "chrome":
        driver = webdriver.Chrome()
    atexit.register(lambda: close_driver(driver))

    # go to the LearnCo login page
    url = "https://learn.co/"
    driver.get(url)

    login_field = driver.find_element_by_css_selector("input#user-email.input__field")
    password_field = driver.find_element_by_css_selector(
        "input#user-password.input__field"
    )
    login_field.send_keys(username)

    # enter password
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # sleep past login page and get the first lesson
    time.sleep(idle_time)
    driver.get(first_lesson)

    # crawl the page
    links = []
    while True:
        time.sleep(idle_time)

        link = get_gitlink(driver)
        links.append(link)
        next_lesson(driver)
        # break if reached final url
        if driver.current_url == last_lesson:
            break
        # break if grabbed too many links
        if len(links) >= lesson_count:
            break

    # close the browser
    driver.close()

    # git clone each link:
    for i, link in enumerate(links):
        next_path = "%s/%03d-%s" % (
            clone_to_path,
            i + 1,
            re.sub(r".+(?<=\/)", "", link),
        )
        run_bash("git clone %s %s" % (link, next_path))


# next_lesson will get the next lesson by attempling to click on the correct
# button to go to the next lesson
def next_lesson(driver):
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


# get_gitlink will get the href attribute of the GitHub button on LearnCo
def get_gitlink(driver):
    return driver.find_element_by_css_selector(
        "a.button--color-grey-faint.button--icon-only"
    ).get_attribute("href")


# close_driver will attempt to close a driver and suppress output
def close_driver(driver):
    try:
        driver.close()
    except:
        pass

if __name__ == "__main__":
    main()
