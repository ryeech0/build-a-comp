from bs4 import BeautifulSoup
import requests

BASELINK = "https://www.vlr.gg/event/agents/"


def scrape_table(soup: BeautifulSoup):
    pass

def create_soup(link: str):
    response = response.get()
    soup = BeautifulSoup(link, "html.parser")
