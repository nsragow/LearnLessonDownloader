from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import system as run_bash
import re


'''
Make sure to edit the following fields!!!!
'''
chromedriver_path = "/Users/noah/Test/chromedriver"
#login credentials for learn
username = "com"
password_text = ""
#the first lesson to clone
start ="https://learn.co/tracks/data-science-career-v2/module-3-probability-sampling-and-ab-testing/section-21-statistical-power-and-anova/introduction"
#the directory to drop all the files into
clone_to_path = "/Users/noah/Flatiron/Lessons/3Module/21section"
if clone_to_path[-1] == "/":
    clone_to_path = clone_to_path[:-1]
#how many lessons to download
lesson_count = 11

driver = webdriver.Chrome(executable_path=chromedriver_path)


url = "https://learn.co/"
driver.get(url)


login = driver.find_element_by_css_selector("input#user-email.input__field")
password = driver.find_element_by_css_selector("input#user-password.input__field")
login.send_keys(username)
password.send_keys(password_text)
password.send_keys(Keys.RETURN)
driver.get(start)
gitlink = driver.find_element_by_css_selector("a.button--color-grey-faint.button--icon-only").get_attribute("href")



proceed_b = "a.js--button.button.module--cloud__button--main"
small_b = "div.js--feature-tour-done-button.js--next-button.status-alert__bubble--with-icon.status-alert__bubble--with-icon--color-inverted.status-alert__bubble--main.hoverable"
big_b = "div.status-alert__button--main.button.button--height-large.button--corners-tight.button--layout-block.js--next-button"
def next_lesson():
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
        print("clicked next")
    except:
        print("no proceed")
def get_gitlink():
    return driver.find_element_by_css_selector("a.button--color-grey-faint.button--icon-only").get_attribute("href")
links = []

def download(index,link):
    next_path = "%s/%03d-%s" % (
        clone_to_path,
        index + 1,
        re.sub(r".+(?<=\/)", "", link),
    )

    run_bash(f"git clone {link} {next_path}")


for x in range(lesson_count):
    next_link = get_gitlink()
    while next_link in links:
        print(f"bad link {next_link}")
        print("waiting...")
        time.sleep(3)
        next_link = get_gitlink()
    links.append(next_link)
    next_lesson()
    download(x,next_link)
