# IMPORTS ==========
import pandas as pd
import numpy as np
import json
from services import scrape


# FUNCTIONS ==========
def read_json_to_df(path: str) -> pd.DataFrame:
    with open(path, "r+") as f:
        data = json.load(f)
        data_df = pd.json_normalize(data, sep="_")
        return data_df

def read_agents_data_from_json():
    with open("resources/agents.json", "r+") as f:
        agents_dict = json.load(f)
        return agents_dict

def get_agents_list():
    agents_dict = read_agents_data_from_json()
    return list(agents_dict.keys())

def get_agent_pickrate(agent: str, map: str):
    df = read_json_to_df("resources/agent_usage_pct.json")
    agent_col = map + "_" + agent
    agent_pickrate_npfloat = df[agent_col][0] # Returns an npfloat
    return agent_pickrate_npfloat.item() # Returns the float value instead of the npfloat

def get_all_agent_pickrates(map: str):
    # Get list of all available agents
    agents = get_agents_list()
    agent_pick_pct_dict = {}

    # Get pickrates of all agents on specific map
    for agent in agents:
        agent_pick_pct_dict[agent] = get_agent_pickrate(agent, map)
    
    return agent_pick_pct_dict

# Calculate winrate of an agent on a specific map
def calculate_agent_winrate(agent: str, map: str):
    # Get shrunken df for the agent on the map specifically
    path = "resources/" + map + ".json"
    df = read_json_to_df(path)
    agent_col = "agent_picks_" + agent
    shrunken_df = df[["match_code", "result", agent_col]]

    # Get percentages
    wins = 0
    losses = 0
    for result, picked in zip(shrunken_df["result"], shrunken_df[agent_col]):
        if result == "win" and picked:
            wins += 1
        elif result == "loss" and picked:
            losses += 1

    # In case the agent hasn't been picked at all on the map, return 0
    if wins + losses == 0:
        return 0.0

    # Calculate percentage
    pct = wins / (wins + losses)
    return pct

def calculate_all_agents_winrates(map: str):
    # Get list of all available agents
    agents = get_agents_list()
    agents_win_pct_dict = {}

    # Get win% of all agents on the map
    for agent in agents:
        agents_win_pct_dict[agent] = calculate_agent_winrate(agent, map)
    
    return agents_win_pct_dict

def calculate_comp_compatibility_score(agents: list):
    pass

# Simple comp generation by statistics
def generate_comp(df: pd.DataFrame, map: str):
    map_col = df[map]
    top_5_agents = map_col.nlargest(5).index.to_list()
    print(top_5_agents)


def main():
    # print(calculate_all_agents_winrates("sunset"))
    print(get_agent_pickrate("chamber", "summit"))

if __name__ == "__main__":
    main()