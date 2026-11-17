# IMPORTS ==========
import pandas as pd
import numpy as np
import json
import scrape


# FUNCTIONS ==========
def read_json_to_df(path) -> pd.DataFrame:
    with open(path, "r+") as f:
        data_df = pd.read_json(path)
        return data_df


def generate_comp(df: pd.DataFrame, map: str):
    map_col = df[map]
    top_5_agents = map_col.nlargest(5).index.to_list()
    print(top_5_agents)




def main():
    agent_usage_pct_df = read_json_to_df("resources/agent_usage_pct.json")
    generate_comp(agent_usage_pct_df, "Lotus")



if __name__ == "__main__":
    main()