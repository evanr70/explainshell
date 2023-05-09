import urllib

import requests
import termcolor
from bs4 import BeautifulSoup


def explain(command: str):
    encoded = urllib.parse.quote(command)

    content = requests.get(f"https://explainshell.com/explain?cmd={encoded}", timeout=3)

    soup = BeautifulSoup(content.content, "html.parser")

    boxes = soup.findAll(class_="help-box")

    for box in boxes:
        print(box.text)
