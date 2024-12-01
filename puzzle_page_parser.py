import os

from bs4 import BeautifulSoup as BS
from pathlib import Path

DAY = os.environ["DAY"]
ADD_TITLE = os.environ.get("ADD_TITLE", False)
ADD_TITLE = (
    ADD_TITLE if isinstance(ADD_TITLE, bool) else ADD_TITLE in ("1", "True", "true")
)

test_input_file = Path("test.txt")
main_file = Path("main.py")
html_file = Path(f"{DAY}.html")
soup = BS(html_file.read_text())

# title
title = soup.select(".day-desc > h2")[0].text
print(title)

# input
code = soup.select("pre > code")[0].text.rstrip("\n")
test_input_file.write_text(code)
print(code)

if not ADD_TITLE:
    exit(0)
with main_file.open("r+") as file:
    contents = file.read()
    if not contents.startswith("# ---"):
        file.seek(0)
        file.write(f"# {title}\n\n")
        file.write(contents)
