# LearnLessonDownloader

# What it does
Will git clone learn lessons in sequence (using the next button) for a specified amount of lessons.<br>
I suggest downloading one section at a time. 

# Warning
If you run this twice without changing the clone_to_path the behavior is unspecified (don't do it).

# How to run
Please edit the top fields (chromedriver_path[path to [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)], <br>
username[for Learn],<br>
password_text[for Learn], <br>
start [URL for the first lesson to download],<br>
clone_to_path [dir where you want the files to drop into], <br>
lesson_count [how many lessons to be downloaded])<br>
if you want the software to run on your machine.
<br>
Otherwise you just need to: `python3 download.py`
in the terminal.

# Dependencies
1. Python3
2. Selenium
3. [Chromedriver dowload](https://sites.google.com/a/chromium.org/chromedriver/)

For chromedriver, make sure to install the driver that matches your chrome version. If you need help check out my [blog](https://nodascience.com/2019/05/19/streamlining-your-chrome-workflow-with-selenium/)

