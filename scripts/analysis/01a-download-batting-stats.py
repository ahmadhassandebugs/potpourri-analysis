import os
from os import path
import requests
from bs4 import BeautifulSoup
import pandas as pd

from utils.context import data_processed_dir

### Config ###
PROCESSED_DATA_FOLDER = path.join(data_processed_dir, "batting-stats")
os.makedirs(PROCESSED_DATA_FOLDER, exist_ok=True)
NUM_PAGES_ESPN_CRICINFO = 4

## format classes as used by espn cricinfo
format_class_dict = {
    "test": 1,
    "odi": 2,
    "t20": 3
}


def get_espn_data_url(format_class="test", play_type="batting",
                      date_start="09+Jul+2013", date_end="09+Jul+2023",
                      data_page=1):
    """
    :param format_class: test/odi/t20
    :param play_type: batting/bowling
    :param date_start:
    :param date_end:
    :param data_page: page # to download from espn (each page has ~50 rows)
    :return: formatted url string to fetch the data
    """
    return (f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class={format_class_dict[format_class]};"
            f"page={data_page};spanmax1={date_end};spanmin1={date_start};spanval1=span;"
            f"template=results;type={play_type}")


def get_espn_format_data(format_class="test", play_type="batting",
                         date_start="09+Jul+2013", date_end="09+Jul+2023",
                         data_pages=1):
    """
    :param format_class: test/odi/t20
    :param play_type: batting/bowling
    :param date_start:
    :param date_end:
    :param data_pages: total pages to download from espn starting from 1 (each page has ~50 rows)
    :return: a DataFrame with data from all pages
    """
    print(f"####### Processing {format_class} data ########")
    df_list = []
    for data_page in range(1, data_pages + 1):
        print(f"downloading page {data_page}...")
        url = get_espn_data_url(format_class, play_type, date_start, date_end, data_page)
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find_all("table", attrs={"class": "engineTable"})[2]

        table_body = table.find("tbody")
        data = []
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values
        header = ["player", "span", "matches", "innings", "notout", "runs", "highestscore", "average", "ballsfaced",
                  "strikerate", "100s", "50s", "0s", "4s", "6s"]
        page_df = pd.DataFrame(data, columns=header)
        df_list.append(page_df)
    df = pd.concat(df_list)
    df = df[["player", "average", "runs", "strikerate"]]
    df = df.astype({"player": "str", "average": "float", "runs": "int", "strikerate": "float"})
    df.sort_values(by=["average", "runs"], ascending=False, inplace=True)
    return df


## download the data
test_df = get_espn_format_data(format_class="test", data_pages=NUM_PAGES_ESPN_CRICINFO)
odi_df = get_espn_format_data(format_class="odi", data_pages=NUM_PAGES_ESPN_CRICINFO)
t20_df = get_espn_format_data(format_class="t20", data_pages=NUM_PAGES_ESPN_CRICINFO)

## save in csv files
test_df.to_csv(path.join(PROCESSED_DATA_FOLDER, "test.csv"), index=False, header=True)
odi_df.to_csv(path.join(PROCESSED_DATA_FOLDER, "odi.csv"), index=False, header=True)
t20_df.to_csv(path.join(PROCESSED_DATA_FOLDER, "t20.csv"), index=False, header=True)

print("Complete../")
