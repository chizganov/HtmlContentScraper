from argparse import ArgumentParser
from scraper import EconHtmlScraper
import os

# Prepare parser
parser = ArgumentParser(description="Extract article from website.")
parser.add_argument("url", metavar='url', type=str, help="an website url")
# Parse arguments
args = parser.parse_args()
url = args.url
# Download html file and extract article text
scraper = EconHtmlScraper(url)
text = scraper.get_text()

base = "../res/"
format = ".txt"
name = url.split("/")[-1]
dir = url.split("://")[1].replace(name, "").replace(".", "_")
if name == "":
    name = "index"
else:
    name = name.split(".")[0].split("?")[0]
# Create directory if not exists
path = base + dir
if not os.path.exists(path):
    os.makedirs(path)

filename = base + dir + name + format
with open(filename, mode="w+", encoding='utf-8') as f:
    f.write(text)
