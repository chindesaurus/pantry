#!/usr/bin/python
import urllib3
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():

    URL = 'https://www.hud.gov/findshelter/Search?search-for=food&place='

    # read in all store zip codes from 'zipCodes.csv' saved down in the same directory

    with open('./zipCodes.csv', 'r', encoding="utf-8") as f:
        for line in f:
            zipCode = line.strip()
            # print(zipCode)

            # grab dynamic html from page
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(URL + zipCode)
                soup = BeautifulSoup(page.content(), "html.parser")
                browser.close()

                soup = soup.find('ul', {"id": 'results'})

                # separate tags with a semicolon
                soup = soup.get_text(separator=';')

                # replace Directions with newline character, strip leading and trailing whitespace
                soup = soup.replace("Directions", "\n")
                soup = soup.strip()

                with open('output.txt', 'a', encoding="utf-8") as o:
                    # write to output file
                    print(soup, "\n", file=o)

                    # write to console for debugging
                    print(soup, "\n")

if __name__ == "__main__":
    main()
