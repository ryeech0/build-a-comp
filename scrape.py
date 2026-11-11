# IMPORTS ==========
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


# CONSTANTS ==========
BASELINK = "https://www.vlr.gg/event/agents/"


# FUNCTIONS ==========
def scrape_tables(soup: BeautifulSoup) -> list:
    tables = soup.find_all("table", class_="wf-table")
    return tables


def parse_usage_table(table) -> pd.DataFrame:
    agent_pct_usage_data: list[dict] = []
    current_maps: list[str] = []
    current_agents: list[str] = []

    # Get agent headers
    header_row = table.find("tr")
    agent_imgs = header_row.find_all("img")
    for agent_img in agent_imgs:
        src = agent_img.get("src")
        filename = src.split("/")[-1]
        agent_name = filename.split(".")[0]
        current_agents.append(agent_name)
    # print(current_agents)

    # Get usage percentages
    for row in table.find_all("tr", class_="pr-global-row"):
        row_cells = row.find_all("td")
        # Get map name (if available)
        map_cell = row_cells[0]
        map_name = map_cell.get_text(strip=True)
        if map_name:
            current_maps.append(map_name[1:])
        else:
            continue
        # print(current_maps)

        # Get usage percentage for each agent and add to a map-dependent dictionary
        map_dict = {}
        for i in range(len(row_cells)-4):
            agent_in_check: str = current_agents[i]
            agent_usage_pct_str: str = row_cells[i+4].get_text(strip=True)
            agent_usage_pct: float = float(agent_usage_pct_str.strip("%")) / 100
            map_dict[agent_in_check] = agent_usage_pct
        # print(map_dict)
        agent_pct_usage_data.append(map_dict)

    # Create dataframe
    agent_usage_pct_df = pd.DataFrame(agent_pct_usage_data, index=current_maps)
    print(agent_usage_pct_df)
    return agent_usage_pct_df


def parse_map_tables(tables):
    pass


def create_soup(link: str):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def update_data():
    pass


def fetch_tables_from_vlr():
    with open("resources/tour_code.json", "r+") as f:
        tour_codes = json.load(f)
        na_oq_code = tour_codes["2026"]["NA_OQ"]
        na_oq_link = BASELINK + str(na_oq_code) + "/"
        turtle_soup = create_soup(na_oq_link)
        vlr_tables = scrape_tables(turtle_soup)
        usage_pct_df = parse_usage_table(vlr_tables[0])
        


# FOR TESTING PURPOSES
if __name__ == "__main__":
    fetch_tables_from_vlr()