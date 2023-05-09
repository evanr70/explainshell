"""Explain a command using explainshell.com."""
import urllib

import requests
from bs4 import BeautifulSoup, Tag

SUCCESS_CODE = 200


def ansi_bold(text: str) -> str:
    """Convert text to bold ansi text."""
    return f"\033[1m{text}\033[0m"


def ansi_underline(text: str) -> str:
    """Convert text to underlined ansi text."""
    return f"\033[4m{text}\033[0m"


def ansi_tag(tag: Tag) -> str:
    """Convert a bs4 tag to ansi text."""
    if not isinstance(tag, Tag):
        return tag
    if tag.name == "b":
        return ansi_bold(tag.text)
    if tag.name == "u":
        return ansi_underline(tag.text)

    return tag.text


def explain(command: str) -> None:
    """Explain a command using explainshell.com."""
    encoded = urllib.parse.quote(command)
    url = f"https://explainshell.com/explain?cmd={encoded}"
    content = requests.get(url, timeout=3)

    if content.status_code != SUCCESS_CODE:
        print("Could not connect to explainshell.com")

    soup = BeautifulSoup(content.content, "html.parser")
    if soup.h4 is not None and soup.h4.text == "missing man page":
        print(
            f"Could not find explaination for {ansi_bold(command)} on explainshell.com",
        )
        return

    boxes = soup.findAll(class_="help-box")
    contents = (box.contents for box in boxes)

    print(f'Explaination for "{ansi_bold(command)}":')
    for content in contents:
        for item in content:
            print(ansi_tag(item), end="")
        print()
    print(f"Source: {ansi_underline(url)}")
