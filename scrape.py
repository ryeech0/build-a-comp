# IMPORTS ==========
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


# CONSTANTS ==========
BASELINK = "https://www.vlr.gg/event/agents/"


# FUNCTIONS ==========
def create_soup(link: str):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def scrape_tables(soup: BeautifulSoup):
    tables = soup.find_all("table", class_="wf-table")
    return tables


# Scrapes usage table data and writes to JSON
def parse_usage_table(table):
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

        # Get usage percentage for each agent and add to a map-dependent dictionary
        map_dict = {}
        for i in range(len(row_cells)-4):
            agent_in_check: str = current_agents[i]
            agent_usage_pct_str: str = row_cells[i+4].get_text(strip=True)
            agent_usage_pct: float = float(agent_usage_pct_str.strip("%")) / 100
            map_dict[agent_in_check] = agent_usage_pct
        agent_pct_usage_data.append(map_dict)

    # Create dataframe
    agent_usage_pct_df = pd.DataFrame(agent_pct_usage_data, index=current_maps)
    print(agent_usage_pct_df)

    # Write to JSON
    agent_usage_pct_df.to_json("resources/agent_usage_pct.json", orient="index", indent=4)


# Scrapes agent pick data per map and writes to separate JSON files
def parse_map_tables(tables):
    for table in tables:
        agent_comp_picks: list[dict] = []
        current_agents: list[str] = []
        current_map: str = ""

        # Get map name & agent headers
        header_row = table.find("tr")
        # Map name
        map_cell = header_row.find("th")
        current_map = map_cell.get_text(strip=True)[1:].lower() # remove the initial letter cuz it's a dupe
        # Agent headers
        agent_imgs = header_row.find_all("img")
        for agent_img in agent_imgs:
            src = agent_img.get("src")
            filename = src.split("/")[-1]
            agent_name = filename.split(".")[0]
            current_agents.append(agent_name)

        # Get agent comp rows
        for row in table.find_all("tr", class_=["pr-matrix-row", "mod-dropdown"]):
            comp_win = True
            comp_dict = {}
            row_cells = row.find_all("td")
            # Get win/loss of comp
            comp_result = row_cells[0].get("class")
            if comp_result == "mod-win":
                comp_win = True
            elif comp_result == "mod-loss":
                comp_win = False
            # Get agents picked
            for i in range(len(row_cells)-2):
                agent_in_check: str = current_agents[i]
                if row_cells[i+2].get("class") == "mod-picked-lite":
                    comp_dict[agent_in_check] = True
                else:
                    comp_dict[agent_in_check] = False
            comp_dict["won"] = comp_win
            agent_comp_picks.append(comp_dict)

        # Create dataframe
        agent_comps_df = pd.DataFrame(agent_comp_picks)
        print(agent_comps_df)

        # Write to JSON
        json_filepath = "resources/" + current_map + ".json"
        agent_comps_df.to_json(json_filepath, orient="records", indent=4)


# Scrape and process vlr tables into JSON files
def process_tables_from_vlr():
    with open("resources/tour_code.json", "r+") as f:
        # Getting the required data
        tour_codes = json.load(f)
        na_oq_code = tour_codes["2026"]["NA_OQ"]
        na_oq_link = BASELINK + str(na_oq_code) + "/"
        turtle_soup = create_soup(na_oq_link)
        # Get all tables
        vlr_tables = scrape_tables(turtle_soup)
        # Agent percentage usage table to JSON
        parse_usage_table(vlr_tables[0])
        # Agent comps for each map to JSON
        parse_map_tables(vlr_tables[1:])

        


# FOR TESTING PURPOSES
if __name__ == "__main__":
    process_tables_from_vlr()